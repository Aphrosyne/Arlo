"""阶段 1 资产库的运行时领域模型。

这些对象只描述扫描结果和本地元数据，不保存数据库 ID，也不访问文件系统。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from domain.tag_ids import normalize_tag_ids


class MetadataState(StrEnum):
    """内容单元旁 ``arlo.ini`` 的读取状态。"""

    MISSING = "missing"
    VALID = "valid"
    INVALID = "invalid"


class ScanIssueSeverity(StrEnum):
    """扫描问题的严重程度。"""

    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class ArloMetadata:
    """``arlo.ini`` 中允许持久化的最小业务元数据。"""

    schema: int
    tags: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema != 1:
            raise ValueError("当前只支持 arlo.ini schema=1")
        object.__setattr__(self, "tags", normalize_tag_ids(self.tags))


@dataclass(frozen=True, slots=True)
class ScannedContentUnit:
    """从现役根目录一级文件夹重建出的运行时内容单元。"""

    name: str
    path: Path
    tags: tuple[str, ...]
    metadata_state: MetadataState

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("内容单元名称不能为空")
        if self.path.name != self.name:
            raise ValueError("内容单元名称必须等于文件夹名")
        object.__setattr__(self, "tags", normalize_tag_ids(self.tags))


@dataclass(frozen=True, slots=True)
class ScanIssue:
    """扫描过程中需要展示给用户的单项问题。"""

    code: str
    path: Path
    message: str
    severity: ScanIssueSeverity = ScanIssueSeverity.ERROR


@dataclass(frozen=True, slots=True)
class AssetLibraryScanResult:
    """一级资产库扫描结果。"""

    root: Path
    content_units: tuple[ScannedContentUnit, ...]
    loose_files: tuple[Path, ...]
    ignored_entries: tuple[Path, ...]
    issues: tuple[ScanIssue, ...]

    @property
    def has_errors(self) -> bool:
        return any(issue.severity is ScanIssueSeverity.ERROR for issue in self.issues)
