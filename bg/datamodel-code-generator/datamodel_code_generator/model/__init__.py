from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from .base import ConstraintsBase, DataModel, DataModelFieldBase

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from datamodel_code_generator.types import DataTypeManager as DataTypeManagerABC


class DataModelSet(NamedTuple):
    data_model: type[DataModel]
    root_model: type[DataModel]
    field_model: type[DataModelFieldBase]
    data_type_manager: type[DataTypeManagerABC]
    dump_resolve_reference_action: Callable[[Iterable[str]], str] | None
    known_third_party: list[str] | None = None


def get_data_model_types(
    data_model_type: DataModelType, target_python_version: PythonVersion
) -> DataModelSet:
    from datamodel_code_generator import DataModelType

    from . import pydantic_v2
    from .types import DataTypeManager

    return DataModelSet(
        data_model=pydantic_v2.BaseModel,
        root_model=pydantic_v2.RootModel,
        field_model=pydantic_v2.DataModelField,
        data_type_manager=pydantic_v2.DataTypeManager,
        dump_resolve_reference_action=pydantic_v2.dump_resolve_reference_action,
    )


__all__ = ["ConstraintsBase", "DataModel", "DataModelFieldBase", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType", "DataModelType"]
