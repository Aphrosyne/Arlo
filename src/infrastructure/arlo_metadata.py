"""``arlo.ini`` 的读写边界。

阶段 1 的内容单元元数据只包含标签和 schema 版本。写入通过同目录临时文件加
``os.replace`` 完成，避免中断时留下半份标签文件。
"""

from __future__ import annotations

import configparser
import contextlib
import os
import tempfile
from pathlib import Path

from domain.asset_library import ArloMetadata
from domain.tag_ids import normalize_tag_ids

ARLO_INI_FILENAME = "arlo.ini"
ARLO_SECTION = "Arlo"
ARLO_SCHEMA = 1
_ALLOWED_OPTIONS = frozenset({"schema", "tags"})


class ArloMetadataError(ValueError):
    """``arlo.ini`` 缺失以外的格式、编码或文件系统错误。"""


def read_arlo_metadata(path: Path) -> ArloMetadata | None:
    """读取一个内容单元的 ``arlo.ini``。

    文件不存在返回 ``None``，表示未整理；文件存在但损坏则抛出可展示的错误。
    """
    if path.is_symlink():
        raise ArloMetadataError("arlo.ini 不能是符号链接")
    if not path.exists():
        return None
    if not path.is_file():
        raise ArloMetadataError("arlo.ini 不是文件")

    parser = configparser.ConfigParser(interpolation=None, strict=True)
    try:
        parser.read(path, encoding="utf-8-sig")
    except (configparser.Error, OSError, UnicodeError) as exc:
        raise ArloMetadataError(f"无法读取 arlo.ini：{exc}") from exc

    if parser.sections() != [ARLO_SECTION]:
        raise ArloMetadataError("arlo.ini 必须只包含 [Arlo] 配置节")

    options = set(parser.options(ARLO_SECTION))
    unknown_options = options - _ALLOWED_OPTIONS
    if unknown_options:
        names = "、".join(sorted(unknown_options))
        raise ArloMetadataError(f"arlo.ini 包含不支持的配置项：{names}")
    if not _ALLOWED_OPTIONS.issubset(options):
        raise ArloMetadataError("arlo.ini 必须包含 schema 和 tags 配置项")

    try:
        schema = parser.getint(ARLO_SECTION, "schema")
        raw_tags = parser.get(ARLO_SECTION, "tags")
        tags = normalize_tag_ids(raw_tags.split(",") if raw_tags.strip() else ())
        return ArloMetadata(schema=schema, tags=tags)
    except (configparser.Error, ValueError) as exc:
        raise ArloMetadataError(f"arlo.ini 内容无效：{exc}") from exc


def write_arlo_metadata(path: Path, tags: list[str] | tuple[str, ...]) -> None:
    """以原子方式写入 ``arlo.ini``。"""
    if path.is_symlink() or (path.exists() and path.is_dir()):
        raise ArloMetadataError("arlo.ini 目标不是普通文件")
    if not path.parent.is_dir():
        raise ArloMetadataError("内容单元目录不存在")

    normalized_tags = normalize_tag_ids(tags)
    text = f"[{ARLO_SECTION}]\nschema={ARLO_SCHEMA}\ntags={','.join(normalized_tags)}\n"
    temporary_path: Path | None = None
    try:
        fd, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as temporary_file:
            temporary_file.write(text)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    except (OSError, UnicodeError) as exc:
        raise ArloMetadataError(f"无法写入 arlo.ini：{exc}") from exc
    finally:
        if temporary_path is not None:
            with contextlib.suppress(OSError):
                temporary_path.unlink(missing_ok=True)
