"""阶段 1 的稳定标签 ID 规则。

标签 ID 是持久化到 ``arlo.ini`` 的机器标识，显示名称由上层标签目录维护。
本模块不访问数据库或文件系统。
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

_TAG_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")


def validate_tag_id(tag_id: str) -> str:
    """校验并返回一个稳定标签 ID。

    ID 使用小写 ASCII，避免显示名称变化或本地化影响 ``arlo.ini`` 内容。
    """
    if not isinstance(tag_id, str) or not _TAG_ID_RE.fullmatch(tag_id):
        raise ValueError(
            "标签 ID 必须是 1-64 个小写 ASCII 字符，并以字母或数字开头；"
            "允许字母、数字、点、下划线和连字符"
        )
    return tag_id


def normalize_tag_ids(tag_ids: Iterable[str]) -> tuple[str, ...]:
    """校验标签 ID、拒绝重复项并返回稳定排序后的元组。"""
    normalized = [validate_tag_id(tag_id.strip()) for tag_id in tag_ids]
    if len(normalized) != len(set(normalized)):
        raise ValueError("标签 ID 不能重复")
    return tuple(sorted(normalized))


@dataclass(frozen=True, slots=True)
class TagDefinition:
    """稳定 ID 与可本地化显示名称的分离定义。"""

    id: str
    display_name: str

    def __post_init__(self) -> None:
        validate_tag_id(self.id)
        if not self.display_name.strip():
            raise ValueError("标签显示名称不能为空")


class TagCatalog:
    """只读标签目录，用于把稳定 ID 映射到显示名称。"""

    def __init__(self, definitions: Iterable[TagDefinition]) -> None:
        definitions_by_id: dict[str, TagDefinition] = {}
        for definition in definitions:
            if definition.id in definitions_by_id:
                raise ValueError(f"标签 ID 重复：{definition.id}")
            definitions_by_id[definition.id] = definition
        self._definitions = definitions_by_id

    def contains(self, tag_id: str) -> bool:
        return tag_id in self._definitions

    def display_name(self, tag_id: str) -> str:
        try:
            return self._definitions[tag_id].display_name
        except KeyError as exc:
            raise KeyError(f"未知标签 ID：{tag_id}") from exc

    def all(self) -> tuple[TagDefinition, ...]:
        return tuple(self._definitions[tag_id] for tag_id in sorted(self._definitions))
