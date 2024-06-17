import re
from collections import defaultdict
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    NamedTuple,
)

from pydantic import Field

from datamodel_code_generator.model.base import UNDEFINED, DataModelFieldBase
from datamodel_code_generator.model.pydantic.base_model import (
    BaseModelBase,
)
from datamodel_code_generator.model.pydantic.base_model import (
    Constraints as _Constraints,
)
from datamodel_code_generator.model.pydantic.base_model import (
    DataModelField as DataModelFieldV1,
)
from datamodel_code_generator.model.pydantic_v2.imports import IMPORT_CONFIG_DICT
from datamodel_code_generator.reference import Reference
from datamodel_code_generator.util import field_validator, model_validator

try:
    from typing import Literal
except ImportError:
    from typing import Literal


class Constraints(_Constraints):
    regex: str | None = Field(None, alias="regex")
    pattern: str | None = Field(None, alias="pattern")

    @model_validator(mode="before")
    def validate_min_max_items(self, values: Any) -> dict[str, Any]:
        if not isinstance(values, dict):
            return values
        min_items = values.pop("minItems", None)
        if min_items is not None:
            values["minLength"] = min_items
        max_items = values.pop("maxItems", None)
        if max_items is not None:
            values["maxLength"] = max_items
        return values


class DataModelField(DataModelFieldV1):
    _EXCLUDE_FIELD_KEYS: ClassVar[set[str]] = {
        "alias",
        "default",
        "gt",
        "ge",
        "lt",
        "le",
        "multiple_of",
        "min_length",
        "max_length",
        "pattern",
    }
    _DEFAULT_FIELD_KEYS: ClassVar[set[str]] = {
        "default",
        "default_factory",
        "alias",
        "alias_priority",
        "validation_alias",
        "serialization_alias",
        "title",
        "description",
        "examples",
        "exclude",
        "discriminator",
        "json_schema_extra",
        "frozen",
        "validate_default",
        "repr",
        "init_var",
        "kw_only",
        "pattern",
        "strict",
        "gt",
        "ge",
        "lt",
        "le",
        "multiple_of",
        "allow_inf_nan",
        "max_digits",
        "decimal_places",
        "min_length",
        "max_length",
        "union_mode",
    }
    constraints: Constraints | None = None
    _PARSE_METHOD: ClassVar[str] = "model_validate"
    can_have_extra_keys: ClassVar[bool] = False

    @field_validator("extras")
    @classmethod
    def validate_extras(cls, values: Any) -> dict[str, Any]:
        if not isinstance(values, dict):
            return values
        if "examples" in values:
            return values

        if "example" in values:
            values["examples"] = [values.pop("example")]
        return values

    def process_const(self) -> None:
        if "const" not in self.extras:
            return
        self.const = True
        self.nullable = False
        const = self.extras["const"]
        self.data_type = self.data_type.__class__(literals=[const])
        if not self.default:
            self.default = const

    def _process_data_in_str(self, data: dict[str, Any]) -> None:
        if self.const:
            data.pop("const")

        data.pop("unique_items", None)

        json_schema_extra = {k: v for k, v in data.items() if k not in self._DEFAULT_FIELD_KEYS}
        if json_schema_extra:
            data["json_schema_extra"] = json_schema_extra
            for key in json_schema_extra:
                data.pop(key)

    def _process_annotated_field_arguments(self, field_arguments: list[str]) -> list[str]:
        if not self.required or self.const:
            if self.use_default_kwarg:
                return [
                    f"default={self.default!r}",
                    *field_arguments,
                ]
            return [f"{self.default!r}", *field_arguments]
        return field_arguments


class ConfigAttribute(NamedTuple):
    from_: str
    to: str
    invert: bool


class BaseModel(BaseModelBase):
    TEMPLATE_FILE_PATH: ClassVar[str] = "pydantic_v2/BaseModel.jinja2"
    BASE_CLASS: ClassVar[str] = "pydantic.BaseModel"
    CONFIG_ATTRIBUTES: ClassVar[list[ConfigAttribute]] = [
        ConfigAttribute("allow_population_by_field_name", "populate_by_name", False),
        ConfigAttribute("populate_by_name", "populate_by_name", False),
        ConfigAttribute("allow_mutation", "frozen", True),
        ConfigAttribute("frozen", "frozen", False),
    ]

    def __init__(
        self,
        *,
        reference: Reference,
        fields: list[DataModelFieldBase],
        decorators: list[str] | None = None,
        base_classes: list[Reference] | None = None,
        custom_base_class: str | None = None,
        custom_template_dir: Path | None = None,
        extra_template_data: defaultdict[str, Any] | None = None,
        path: Path | None = None,
        description: str | None = None,
        default: Any = UNDEFINED,
        nullable: bool = False,
    ) -> None:
        super().__init__(
            reference=reference,
            fields=fields,
            decorators=decorators,
            base_classes=base_classes,
            custom_base_class=custom_base_class,
            custom_template_dir=custom_template_dir,
            extra_template_data=extra_template_data,
            path=path,
            description=description,
            default=default,
            nullable=nullable,
        )
        config_parameters: dict[str, Any] = {}

        extra = self._get_config_extra()
        if extra:
            config_parameters["extra"] = extra

        for from_, to, invert in self.CONFIG_ATTRIBUTES:
            if from_ in self.extra_template_data:
                config_parameters[to] = (
                    not self.extra_template_data[from_] if invert else self.extra_template_data[from_]
                )
        for data_type in self.all_data_types:
            if data_type.is_custom_type:
                config_parameters["arbitrary_types_allowed"] = True
                break

        for field in self.fields:
            pattern = (isinstance(field.constraints, Constraints) and field.constraints.pattern) or (
                field.data_type.kwargs or {}
            ).get("pattern")
            if pattern and re.search(r"\(\?<?[=!]", pattern):
                config_parameters["regex_engine"] = '"python-re"'
                break

        if isinstance(self.extra_template_data.get("config"), dict):
            for key, value in self.extra_template_data["config"].items():
                config_parameters[key] = value

        if config_parameters:
            from datamodel_code_generator.model.pydantic_v2 import ConfigDict

            self.extra_template_data["config"] = ConfigDict.parse_obj(config_parameters)
            self._additional_imports.append(IMPORT_CONFIG_DICT)

    def _get_config_extra(self) -> Literal["'allow'", "'forbid'"] | None:
        additionalProperties = self.extra_template_data.get("additionalProperties")
        allow_extra_fields = self.extra_template_data.get("allow_extra_fields")
        if additionalProperties is not None or allow_extra_fields:
            return "'allow'" if additionalProperties or allow_extra_fields else "'forbid'"
        return None
