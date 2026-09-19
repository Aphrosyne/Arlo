"""阶段 1 资产库应用服务测试。"""

from __future__ import annotations

from pathlib import Path

import pytest

from application.asset_library_service import AssetLibraryMetadataError, AssetLibraryService


def test_save_tags_writes_through_application_service(tmp_path: Path) -> None:
    unit_path = tmp_path / "My Unit"
    unit_path.mkdir()

    AssetLibraryService().save_tags(unit_path, ["ube"])

    assert (unit_path / "arlo.ini").read_text(encoding="utf-8") == ("[Arlo]\nschema=1\ntags=ube\n")


def test_save_tags_rejects_non_directory(tmp_path: Path) -> None:
    with pytest.raises(AssetLibraryMetadataError, match="不存在或不是普通目录"):
        AssetLibraryService().save_tags(tmp_path / "missing", ["ube"])


def test_scan_index_is_rebuildable_and_supports_filtering(tmp_path: Path) -> None:
    root = tmp_path / "ManagedLibrary"
    unit_path = root / "My Outfit"
    unit_path.mkdir(parents=True)
    (unit_path / "arlo.ini").write_text("[Arlo]\nschema=1\ntags=clothing,ube\n", encoding="utf-8")
    (root / "Weapon").mkdir()

    index = AssetLibraryService().scan_index(root)

    assert index.find_by_path(Path(str(unit_path))) is not None
    assert [unit.name for unit in index.filter_by_tags(["ube"])] == ["My Outfit"]
    assert [unit.name for unit in index.search("outfit")] == ["My Outfit"]
    assert [unit.name for unit in index.search("UBE")] == ["My Outfit"]
    rebuilt = AssetLibraryService().scan_index(root)
    assert rebuilt.content_units == index.content_units


def test_scan_index_handles_unicode_names_and_normalized_paths(tmp_path: Path) -> None:
    root = tmp_path / "中文资产库"
    unit_path = root / "服装测试"
    unit_path.mkdir(parents=True)

    index = AssetLibraryService().scan_index(root)

    assert index.find_by_path(root / "." / unit_path.name) is not None
    assert [unit.name for unit in index.search("服装")] == ["服装测试"]


def test_save_tags_reports_duplicate_ids_without_creating_metadata(tmp_path: Path) -> None:
    unit_path = tmp_path / "Duplicate Tags"
    unit_path.mkdir()

    with pytest.raises(AssetLibraryMetadataError, match="不能重复"):
        AssetLibraryService().save_tags(unit_path, ["ube", "ube"])

    assert not (unit_path / "arlo.ini").exists()
