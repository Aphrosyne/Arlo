"""阶段 1 固定初始标签目录测试。"""

from __future__ import annotations

from domain.initial_tags import INITIAL_TAG_CATALOG, INITIAL_TAG_DEFINITIONS


def test_initial_catalog_is_flat_and_contains_fifteen_tags() -> None:
    definitions = INITIAL_TAG_CATALOG.all()

    assert len(definitions) == 15
    assert definitions == tuple(sorted(definitions, key=lambda definition: definition.id))
    assert {definition.display_name for definition in definitions} == {
        "核心框架",
        "补丁兼容",
        "角色美化",
        "装备物品",
        "武器",
        "动画动作",
        "物理系统",
        "世界环境",
        "玩法系统",
        "任务地点",
        "NPC 与生物",
        "UI 界面",
        "音效音乐",
        "画面渲染",
        "其他杂项",
    }
    assert all("." not in definition.id for definition in INITIAL_TAG_DEFINITIONS)
