from __future__ import annotations

from typing import Callable, Iterable, List, NamedTuple, Optional, Type

from ..types import DataTypeManager as DataTypeManagerABC
from .base import ConstraintsBase, DataModel, DataModelFieldBase


class DataModelSet(NamedTuple):
    data_model: Type[DataModel]
    root_model: Type[DataModel]
    field_model: Type[DataModelFieldBase]
    data_type_manager: Type[DataTypeManagerABC]
    dump_resolve_reference_action: Optional[Callable[[Iterable[str]], str]]
    known_third_party: Optional[List[str]] = None


def get_data_model_types(
    data_model_type: DataModelType, target_python_version: PythonVersion
) -> DataModelSet:
    from .. import DataModelType
    from . import pydantic_v2
    from .types import DataTypeManager

    return DataModelSet(
        data_model=pydantic_v2.BaseModel,
        root_model=pydantic_v2.RootModel,
        field_model=pydantic_v2.DataModelField,
        data_type_manager=pydantic_v2.DataTypeManager,
        dump_resolve_reference_action=pydantic_v2.dump_resolve_reference_action,
    )


__all__ = ["ConstraintsBase", "DataModel", "DataModelFieldBase"]
