"""阶段 1 arlo.ini 读写测试。"""

from __future__ import annotations

from pathlib import Path

import pytest

from infrastructure.arlo_metadata import ArloMetadataError, read_arlo_metadata, write_arlo_metadata


def test_missing_metadata_means_un整理(tmp_path: Path) -> None:
    assert read_arlo_metadata(tmp_path / "arlo.ini") is None


def test_write_and_read_metadata_uses_sorted_stable_ids(tmp_path: Path) -> None:
    metadata_path = tmp_path / "arlo.ini"
    write_arlo_metadata(metadata_path, ["ube", "clothing"])

    assert metadata_path.read_text(encoding="utf-8") == "[Arlo]\nschema=1\ntags=clothing,ube\n"
    metadata = read_arlo_metadata(metadata_path)
    assert metadata is not None
    assert metadata.schema == 1
    assert metadata.tags == ("clothing", "ube")


@pytest.mark.parametrize(
    ("contents", "message"),
    [
        ("[Arlo]\nschema=2\ntags=clothing\n", "schema"),
        ("[Arlo]\nschema=1\ntags=中文\n", "内容无效"),
        ("[Arlo]\nschema=1\ntags=ube,ube\n", "内容无效"),
        ("[Other]\nschema=1\ntags=clothing\n", "必须只包含"),
        ("[Arlo]\nschema=1\ntags=clothing\nextra=value\n", "不支持"),
    ],
)
def test_invalid_metadata_is_reported(tmp_path: Path, contents: str, message: str) -> None:
    metadata_path = tmp_path / "arlo.ini"
    metadata_path.write_text(contents, encoding="utf-8")

    with pytest.raises(ArloMetadataError, match=message):
        read_arlo_metadata(metadata_path)


def test_write_requires_existing_content_unit_directory(tmp_path: Path) -> None:
    with pytest.raises(ArloMetadataError, match="目录不存在"):
        write_arlo_metadata(tmp_path / "missing" / "arlo.ini", ["clothing"])
