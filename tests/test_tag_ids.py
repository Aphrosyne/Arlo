"""阶段 1 稳定标签 ID 测试。"""

from __future__ import annotations

import pytest

from domain.tag_ids import TagCatalog, TagDefinition, normalize_tag_ids, validate_tag_id


@pytest.mark.parametrize("tag_id", ["clothing", "ube", "magic.spells", "body_hair-1"])
def test_validate_tag_id_accepts_stable_ascii_ids(tag_id: str) -> None:
    assert validate_tag_id(tag_id) == tag_id


@pytest.mark.parametrize("tag_id", ["", "中文", "Clothing", "-clothing", "has space"])
def test_validate_tag_id_rejects_display_names_and_invalid_ids(tag_id: str) -> None:
    with pytest.raises(ValueError):
        validate_tag_id(tag_id)


def test_normalize_tag_ids_sorts_and_rejects_duplicates() -> None:
    assert normalize_tag_ids(["ube", "clothing"]) == ("clothing", "ube")
    with pytest.raises(ValueError, match="不能重复"):
        normalize_tag_ids(["ube", "ube"])


def test_tag_catalog_keeps_display_names_separate() -> None:
    catalog = TagCatalog(
        [
            TagDefinition(id="clothing", display_name="服装"),
            TagDefinition(id="ube", display_name="UBE"),
        ]
    )
    assert catalog.display_name("clothing") == "服装"
    assert catalog.all()[0].id == "clothing"
    with pytest.raises(KeyError, match="未知标签 ID"):
        catalog.display_name("missing")
