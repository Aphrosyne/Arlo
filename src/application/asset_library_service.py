"""阶段 1 资产库应用服务。

该服务为 UI 提供扫描、索引建立和扁平初始标签写入边界，不直接暴露旧数据库 ContentUnit 流程。
"""

from __future__ import annotations

from pathlib import Path

from application.asset_library_index import AssetLibraryIndex
from application.errors import ApplicationError
from domain.asset_library import AssetLibraryScanResult
from domain.initial_tags import INITIAL_TAG_CATALOG
from domain.tag_ids import TagCatalog, TagDefinition
from infrastructure.arlo_metadata import (
    ARLO_INI_FILENAME,
    ArloMetadataError,
    read_arlo_metadata,
    write_arlo_metadata,
)
from infrastructure.asset_library_scanner import AssetLibraryScanner


class AssetLibraryMetadataError(ApplicationError):
    """内容单元标签文件读写失败。"""


class AssetLibraryTagError(ApplicationError):
    """标签不属于阶段 1 固定初始标签目录。"""


class AssetLibraryService:
    """协调现役资产库扫描、索引建立和初始标签写入。"""

    def __init__(
        self,
        scanner: AssetLibraryScanner | None = None,
        tag_catalog: TagCatalog = INITIAL_TAG_CATALOG,
    ) -> None:
        self._scanner = scanner or AssetLibraryScanner()
        self._tag_catalog = tag_catalog

    def scan(self, root: Path) -> AssetLibraryScanResult:
        """扫描现役根目录，结果可直接由文件系统重建。"""
        return self._scanner.scan(root)

    def scan_index(self, root: Path) -> AssetLibraryIndex:
        """扫描并建立一个可丢弃、可重建的运行时索引。"""
        return AssetLibraryIndex.from_scan(self.scan(root))

    def available_tags(self) -> tuple[TagDefinition, ...]:
        """返回阶段 1 固定的初始标签目录。"""
        return self._tag_catalog.all()

    def add_tag(self, content_unit_path: Path, tag_id: str) -> None:
        """为内容单元添加一个初始标签；重复添加保持幂等。"""
        self._validate_tag_id(tag_id)
        current_tags = self._read_tags(content_unit_path)
        if tag_id in current_tags:
            return
        self.save_tags(content_unit_path, (*current_tags, tag_id))

    def remove_tag(self, content_unit_path: Path, tag_id: str) -> None:
        """从内容单元移除一个初始标签；移除不存在的标签保持幂等。"""
        self._validate_tag_id(tag_id)
        current_tags = self._read_tags(content_unit_path)
        if tag_id not in current_tags:
            return
        self.save_tags(content_unit_path, tuple(tag for tag in current_tags if tag != tag_id))

    def save_tags(self, content_unit_path: Path, tags: list[str] | tuple[str, ...]) -> None:
        """为现有内容单元保存标签。"""
        self._validate_content_unit_path(content_unit_path)
        try:
            write_arlo_metadata(content_unit_path / ARLO_INI_FILENAME, tags)
        except ArloMetadataError as exc:
            raise AssetLibraryMetadataError(str(exc)) from exc

    def _read_tags(self, content_unit_path: Path) -> tuple[str, ...]:
        self._validate_content_unit_path(content_unit_path)
        try:
            metadata = read_arlo_metadata(content_unit_path / ARLO_INI_FILENAME)
        except ArloMetadataError as exc:
            raise AssetLibraryMetadataError(str(exc)) from exc
        return () if metadata is None else metadata.tags

    def _validate_tag_id(self, tag_id: str) -> None:
        if not self._tag_catalog.contains(tag_id):
            raise AssetLibraryTagError(f"标签不在阶段 1 初始目录中：{tag_id}")

    @staticmethod
    def _validate_content_unit_path(content_unit_path: Path) -> None:
        if not content_unit_path.is_dir() or content_unit_path.is_symlink():
            raise AssetLibraryMetadataError("内容单元路径不存在或不是普通目录")
