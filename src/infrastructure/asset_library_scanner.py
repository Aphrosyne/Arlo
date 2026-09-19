"""现役资产根目录的一级只读扫描器。"""

from __future__ import annotations

import os
import stat
from pathlib import Path

from domain.asset_library import (
    AssetLibraryScanResult,
    MetadataState,
    ScanIssue,
    ScanIssueSeverity,
    ScannedContentUnit,
)
from infrastructure.arlo_metadata import ARLO_INI_FILENAME, ArloMetadataError, read_arlo_metadata

_FILE_ATTRIBUTE_HIDDEN = 0x2
_FILE_ATTRIBUTE_SYSTEM = 0x4


class AssetLibraryScanner:
    """只读取现役根目录本身，不递归读取内容单元内部文件。"""

    def scan(self, root: Path) -> AssetLibraryScanResult:
        content_units: list[ScannedContentUnit] = []
        loose_files: list[Path] = []
        ignored_entries: list[Path] = []
        issues: list[ScanIssue] = []

        if root.is_symlink():
            issues.append(ScanIssue("root_symlink", root, "现役资产根目录不能是符号链接"))
            return self._result(root, content_units, loose_files, ignored_entries, issues)
        if not root.exists():
            issues.append(ScanIssue("root_missing", root, "现役资产根目录不存在"))
            return self._result(root, content_units, loose_files, ignored_entries, issues)
        if not root.is_dir():
            issues.append(ScanIssue("root_not_directory", root, "现役资产根路径不是目录"))
            return self._result(root, content_units, loose_files, ignored_entries, issues)

        try:
            entries = sorted(root.iterdir(), key=lambda entry: (entry.name.casefold(), entry.name))
        except OSError as exc:
            issues.append(ScanIssue("root_unreadable", root, f"无法读取现役资产根目录：{exc}"))
            return self._result(root, content_units, loose_files, ignored_entries, issues)

        for entry in entries:
            try:
                entry_stat = entry.lstat()
            except OSError as exc:
                issues.append(ScanIssue("entry_unreadable", entry, f"无法读取目录条目：{exc}"))
                continue

            if entry.is_symlink():
                ignored_entries.append(entry)
                issues.append(
                    ScanIssue(
                        "symlink_ignored",
                        entry,
                        "已忽略符号链接条目",
                        ScanIssueSeverity.WARNING,
                    )
                )
                continue
            if self._is_hidden_or_system(entry, entry_stat):
                ignored_entries.append(entry)
                issues.append(
                    ScanIssue(
                        "hidden_entry_ignored",
                        entry,
                        "已忽略隐藏或系统条目",
                        ScanIssueSeverity.WARNING,
                    )
                )
                continue

            mode = entry_stat.st_mode
            if stat.S_ISDIR(mode):
                content_units.append(self._scan_content_unit(entry, issues))
            elif stat.S_ISREG(mode):
                loose_files.append(entry)
            else:
                ignored_entries.append(entry)
                issues.append(
                    ScanIssue(
                        "unsupported_entry",
                        entry,
                        "已忽略不支持的文件系统条目",
                        ScanIssueSeverity.WARNING,
                    )
                )

        return self._result(root, content_units, loose_files, ignored_entries, issues)

    def _scan_content_unit(self, path: Path, issues: list[ScanIssue]) -> ScannedContentUnit:
        metadata_path = path / ARLO_INI_FILENAME
        try:
            metadata = read_arlo_metadata(metadata_path)
        except ArloMetadataError as exc:
            issues.append(ScanIssue("invalid_metadata", metadata_path, str(exc)))
            return ScannedContentUnit(
                name=path.name,
                path=path,
                tags=(),
                metadata_state=MetadataState.INVALID,
            )

        if metadata is None:
            return ScannedContentUnit(
                name=path.name,
                path=path,
                tags=(),
                metadata_state=MetadataState.MISSING,
            )
        return ScannedContentUnit(
            name=path.name,
            path=path,
            tags=metadata.tags,
            metadata_state=MetadataState.VALID,
        )

    @staticmethod
    def _is_hidden_or_system(path: Path, entry_stat: os.stat_result) -> bool:
        if path.name.startswith("."):
            return True
        attributes = getattr(entry_stat, "st_file_attributes", 0)
        return bool(attributes & (_FILE_ATTRIBUTE_HIDDEN | _FILE_ATTRIBUTE_SYSTEM))

    @staticmethod
    def _result(
        root: Path,
        content_units: list[ScannedContentUnit],
        loose_files: list[Path],
        ignored_entries: list[Path],
        issues: list[ScanIssue],
    ) -> AssetLibraryScanResult:
        return AssetLibraryScanResult(
            root=root,
            content_units=tuple(content_units),
            loose_files=tuple(loose_files),
            ignored_entries=tuple(ignored_entries),
            issues=tuple(issues),
        )
