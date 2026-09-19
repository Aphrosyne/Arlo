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
