"""阶段 1 一级资产库扫描测试。"""

from __future__ import annotations

from pathlib import Path

from domain.asset_library import MetadataState
from infrastructure.asset_library_scanner import AssetLibraryScanner


def test_scan_reads_only_first_level_units_and_reports_loose_files(tmp_path: Path) -> None:
    root = tmp_path / "ManagedLibrary"
    root.mkdir()
    alpha = root / "Alpha"
    alpha.mkdir()
    (alpha / "arlo.ini").write_text("[Arlo]\nschema=1\ntags=ube,clothing\n", encoding="utf-8")
    (alpha / "nested").mkdir()
    (alpha / "nested" / "deep-file.esp").write_text("not scanned", encoding="utf-8")
    beta = root / "Beta"
    beta.mkdir()
    (root / "loose.7z").write_text("not scanned", encoding="utf-8")
    hidden = root / ".hidden"
    hidden.mkdir()

    result = AssetLibraryScanner().scan(root)

    assert [unit.name for unit in result.content_units] == ["Alpha", "Beta"]
    assert result.content_units[0].tags == ("clothing", "ube")
    assert result.content_units[0].metadata_state is MetadataState.VALID
    assert result.content_units[1].metadata_state is MetadataState.MISSING
    assert result.loose_files == (root / "loose.7z",)
    assert result.ignored_entries == (hidden,)
    assert not any(path.name == "deep-file.esp" for path in result.loose_files)
    assert any(issue.code == "hidden_entry_ignored" for issue in result.issues)
    assert not result.has_errors


def test_scan_keeps_invalid_metadata_unit_visible_and_reports_issue(tmp_path: Path) -> None:
    root = tmp_path / "ManagedLibrary"
    broken = root / "Broken"
    broken.mkdir(parents=True)
    (broken / "arlo.ini").write_text("[Arlo]\nschema=1\ntags=中文\n", encoding="utf-8")

    result = AssetLibraryScanner().scan(root)

    assert len(result.content_units) == 1
    assert result.content_units[0].metadata_state is MetadataState.INVALID
    assert result.content_units[0].tags == ()
    assert any(issue.code == "invalid_metadata" for issue in result.issues)
    assert result.has_errors


def test_scan_reports_missing_or_invalid_root_without_writing(tmp_path: Path) -> None:
    missing = tmp_path / "missing"
    result = AssetLibraryScanner().scan(missing)
    assert result.content_units == ()
    assert result.issues[0].code == "root_missing"

    file_root = tmp_path / "not-a-root.txt"
    file_root.write_text("x", encoding="utf-8")
    result = AssetLibraryScanner().scan(file_root)
    assert result.issues[0].code == "root_not_directory"
