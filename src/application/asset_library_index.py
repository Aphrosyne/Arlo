"""阶段 1 资产库运行时内存索引。"""

from __future__ import annotations

from pathlib import Path

from domain.asset_library import AssetLibraryScanResult, ScannedContentUnit
from domain.tag_ids import normalize_tag_ids
from infrastructure.path_utils import make_path_key


class AssetLibraryIndex:
    """由一次只读扫描结果重建的内存索引。

    索引不是持久化事实来源；重新扫描即可重建全部内容。它不持有数据库、
    目录树、操作历史或多根目录服务。
    """

    def __init__(self, result: AssetLibraryScanResult) -> None:
        self.root = result.root
        self.content_units = result.content_units
        self.loose_files = result.loose_files
        self.ignored_entries = result.ignored_entries
        self.issues = result.issues
        self._units_by_path_key = {make_path_key(unit.path): unit for unit in self.content_units}

    @classmethod
    def from_scan(cls, result: AssetLibraryScanResult) -> AssetLibraryIndex:
        return cls(result)

    def find_by_path(self, path: Path) -> ScannedContentUnit | None:
        """按规范化路径查找内容单元。"""
        return self._units_by_path_key.get(make_path_key(path))

    def filter_by_tags(
        self, tag_ids: list[str] | tuple[str, ...]
    ) -> tuple[ScannedContentUnit, ...]:
        """返回包含全部指定标签的内容单元。"""
        required = set(normalize_tag_ids(tag_ids))
        if not required:
            return self.content_units
        return tuple(unit for unit in self.content_units if required.issubset(unit.tags))

    def search(self, query: str) -> tuple[ScannedContentUnit, ...]:
        """按文件夹名称或稳定标签 ID 进行简单不区分大小写搜索。"""
        normalized_query = query.strip().casefold()
        if not normalized_query:
            return self.content_units
        return tuple(
            unit
            for unit in self.content_units
            if normalized_query in unit.name.casefold()
            or any(normalized_query in tag_id.casefold() for tag_id in unit.tags)
        )
