from __future__ import annotations

from pydantic import BaseModel as _BaseModel

from .base_model import BaseModel, DataModelField
from .custom_root_type import CustomRootType
from .dataclass import DataClass
from .types import DataTypeManager


class Config(_BaseModel):
    extra: str | None = None
    title: str | None = None
    allow_population_by_field_name: bool | None = None
    allow_extra_fields: bool | None = None
    allow_mutation: bool | None = None
    arbitrary_types_allowed: bool | None = None
    orm_mode: bool | None = None


__all__ = [
    "BaseModel",
    "CustomRootType",
    "DataClass",
    "DataModelField",
    "DataTypeManager",
]
