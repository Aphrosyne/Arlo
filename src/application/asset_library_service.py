"""阶段 1 资产库应用服务。

该服务为 UI 提供扫描和标签写入边界，不直接暴露旧数据库 ContentUnit 流程。
"""

from __future__ import annotations

from pathlib import Path

from application.errors import ApplicationError
from domain.asset_library import AssetLibraryScanResult
from infrastructure.arlo_metadata import ARLO_INI_FILENAME, ArloMetadataError, write_arlo_metadata
from infrastructure.asset_library_scanner import AssetLibraryScanner


class AssetLibraryMetadataError(ApplicationError):
    """内容单元标签文件读写失败。"""


class AssetLibraryService:
    """协调现役资产库扫描和内容单元标签写入。"""

    def __init__(self, scanner: AssetLibraryScanner | None = None) -> None:
        self._scanner = scanner or AssetLibraryScanner()

    def scan(self, root: Path) -> AssetLibraryScanResult:
        """扫描现役根目录，结果可直接由文件系统重建。"""
        return self._scanner.scan(root)

    def save_tags(self, content_unit_path: Path, tags: list[str] | tuple[str, ...]) -> None:
        """为现有内容单元保存标签。"""
        if not content_unit_path.is_dir() or content_unit_path.is_symlink():
            raise AssetLibraryMetadataError("内容单元路径不存在或不是普通目录")
        try:
            write_arlo_metadata(content_unit_path / ARLO_INI_FILENAME, tags)
        except ArloMetadataError as exc:
            raise AssetLibraryMetadataError(str(exc)) from exc
