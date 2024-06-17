from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel

from .base_model import BaseModel, DataModelField
from .root_model import RootModel
from .types import DataTypeManager

if TYPE_CHECKING:
    from collections.abc import Iterable


def dump_resolve_reference_action(class_names: Iterable[str]) -> str:
    return "\n".join(f"{class_name}.model_rebuild()" for class_name in class_names)


class ConfigDict(_BaseModel):
    extra: str | None = None
    title: str | None = None
    populate_by_name: bool | None = None
    allow_extra_fields: bool | None = None
    from_attributes: bool | None = None
    frozen: bool | None = None
    arbitrary_types_allowed: bool | None = None
    protected_namespaces: tuple[str, ...] | None = None
    regex_engine: str | None = None


__all__ = [
    "BaseModel",
    "DataModelField",
    "DataTypeManager",
    "RootModel",
    "dump_resolve_reference_action",
]
