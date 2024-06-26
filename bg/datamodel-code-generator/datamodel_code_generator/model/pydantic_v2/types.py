from __future__ import annotations

from typing import ClassVar

from datamodel_code_generator.model.pydantic import DataTypeManager as _DataTypeManager
from datamodel_code_generator.model.pydantic.imports import IMPORT_CONSTR
from datamodel_code_generator.model.pydantic_v2.imports import IMPORT_AWARE_DATETIME
from datamodel_code_generator.types import DataType, StrictTypes, Types

from collections.abc import Sequence


class DataTypeManager(_DataTypeManager):
    PATTERN_KEY: ClassVar[str] = "pattern"

    def type_map_factory(
        self,
        data_type: type[DataType],
        strict_types: Sequence[StrictTypes],
        pattern_key: str,
    ) -> dict[Types, DataType]:
        return {
            **super().type_map_factory(data_type, strict_types, pattern_key),
            Types.hostname: self.data_type.from_import(
                IMPORT_CONSTR,
                strict=StrictTypes.str in strict_types,
                kwargs={
                    pattern_key: r"r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]{0,61}[A-Za-z0-9])$'",
                    **({"strict": True} if StrictTypes.str in strict_types else {}),
                },
            ),
            Types.date_time: data_type.from_import(IMPORT_AWARE_DATETIME),
        }
