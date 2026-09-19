"""阶段 1 的固定初始标签目录。

初始标签是扁平集合，不包含分类、层级或应用内管理配置。作者和来源不在本目录中。
"""

from __future__ import annotations

from domain.tag_ids import TagCatalog, TagDefinition

INITIAL_TAG_DEFINITIONS = (
    TagDefinition(id="core_framework", display_name="核心框架"),
    TagDefinition(id="patches", display_name="补丁兼容"),
    TagDefinition(id="character_appearance", display_name="角色美化"),
    TagDefinition(id="equipment", display_name="装备物品"),
    TagDefinition(id="weapons", display_name="武器"),
    TagDefinition(id="animation", display_name="动画动作"),
    TagDefinition(id="physics", display_name="物理系统"),
    TagDefinition(id="world", display_name="世界环境"),
    TagDefinition(id="gameplay", display_name="玩法系统"),
    TagDefinition(id="quests_locations", display_name="任务地点"),
    TagDefinition(id="npc_creatures", display_name="NPC 与生物"),
    TagDefinition(id="ui", display_name="UI 界面"),
    TagDefinition(id="audio", display_name="音效音乐"),
    TagDefinition(id="visuals", display_name="画面渲染"),
    TagDefinition(id="miscellaneous", display_name="其他杂项"),
)

INITIAL_TAG_CATALOG = TagCatalog(INITIAL_TAG_DEFINITIONS)
