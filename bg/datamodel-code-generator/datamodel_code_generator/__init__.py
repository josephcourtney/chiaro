import contextlib
import os
import sys
from collections import defaultdict
from collections.abc import Callable, Iterator, Mapping, Sequence
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import (
    IO,
    Any,
    TextIO,
    TypeVar,
)
from urllib.parse import ParseResult

import yaml

from datamodel_code_generator.format import PythonVersion
from datamodel_code_generator.model import get_data_model_types
from datamodel_code_generator.parser import DefaultPutDict, LiteralType
from datamodel_code_generator.types import StrictTypes
from datamodel_code_generator.util import SafeLoader

T = TypeVar("T")


DEFAULT_BASE_CLASS: str = "pydantic.BaseModel"


def load_yaml(stream: str | TextIO) -> Any:
    return yaml.load(stream, Loader=SafeLoader)






@contextlib.contextmanager
def chdir(path: Path | None) -> Iterator[None]:
    prev_cwd = Path.cwd()
    try:
        os.chdir(path if path.is_dir() else path.parent)
        yield
    finally:
        os.chdir(prev_cwd)




JSON_SCHEMA_URLS: tuple[str, ...] = (
    "http://json-schema.org/",
    "https://json-schema.org/",
)



class InputFileType(Enum):
    Auto = "auto"
    OpenAPI = "openapi"
    JsonSchema = "jsonschema"
    Json = "json"
    Yaml = "yaml"
    Dict = "dict"
    CSV = "csv"
    GraphQL = "graphql"


RAW_DATA_TYPES: list[InputFileType] = [
    InputFileType.Json,
    InputFileType.Yaml,
    InputFileType.Dict,
    InputFileType.CSV,
    InputFileType.GraphQL,
]


class DataModelType(Enum):
    PydanticBaseModel = "pydantic.BaseModel"
    PydanticV2BaseModel = "pydantic_v2.BaseModel"
    DataclassesDataclass = "dataclasses.dataclass"
    TypingTypedDict = "typing.TypedDict"
    MsgspecStruct = "msgspec.Struct"


class OpenAPIScope(Enum):
    Schemas = "schemas"
    Paths = "paths"
    Tags = "tags"
    Parameters = "parameters"


class GraphQLScope(Enum):
    Schema = "schema"


class Error(Exception):
    def __init__(self, message: str) -> None: ...

    def __str__(self) -> str: ...


class InvalidClassNameError(Error):
    def __init__(self, class_name: str) -> None: ...



def generate(
    input_: Path | str | ParseResult,
    *,
    input_filename: str | None = None,
    input_file_type: InputFileType = InputFileType.Auto,
    output: Path | None = None,
    output_model_type: DataModelType = DataModelType.PydanticBaseModel,
    target_python_version: PythonVersion = PythonVersion.PY_37,
    base_class: str = "",
    additional_imports: list[str] | None = None,
    custom_template_dir: Path | None = None,
    extra_template_data: defaultdict[str, dict[str, Any]] | None = None,
    validation: bool = False,
    field_constraints: bool = False,
    snake_case_field: bool = False,
    strip_default_none: bool = False,
    aliases: Mapping[str, str] | None = None,
    disable_timestamp: bool = False,
    enable_version_header: bool = False,
    allow_population_by_field_name: bool = False,
    allow_extra_fields: bool = False,
    apply_default_values_for_required_fields: bool = False,
    force_optional_for_required_fields: bool = False,
    class_name: str | None = None,
    use_standard_collections: bool = False,
    use_schema_description: bool = False,
    use_field_description: bool = False,
    use_default_kwarg: bool = False,
    reuse_model: bool = False,
    encoding: str = "utf-8",
    enum_field_as_literal: LiteralType | None = None,
    use_one_literal_as_default: bool = False,
    set_default_enum_member: bool = False,
    use_subclass_enum: bool = False,
    strict_nullable: bool = False,
    use_generic_container_types: bool = False,
    enable_faux_immutability: bool = False,
    disable_appending_item_suffix: bool = False,
    strict_types: Sequence[StrictTypes] | None = None,
    empty_enum_field_name: str | None = None,
    custom_class_name_generator: Callable[[str], str] | None = None,
    field_extra_keys: set[str] | None = None,
    field_include_all_keys: bool = False,
    field_extra_keys_without_x_prefix: set[str] | None = None,
    openapi_scopes: list[OpenAPIScope] | None = None,
    wrap_string_literal: bool | None = None,
    use_title_as_name: bool = False,
    use_operation_id_as_name: bool = False,
    use_unique_items_as_set: bool = False,
    http_headers: Sequence[tuple[str, str]] | None = None,
    http_ignore_tls: bool = False,
    use_annotated: bool = False,
    use_non_positive_negative_number_constrained_types: bool = False,
    original_field_name_delimiter: str | None = None,
    use_double_quotes: bool = False,
    use_union_operator: bool = False,
    collapse_root_models: bool = False,
    special_field_name_prefix: str | None = None,
    remove_special_field_name_prefix: bool = False,
    capitalise_enum_members: bool = False,
    keep_model_order: bool = False,
    custom_file_header: str | None = None,
    custom_file_header_path: Path | None = None,
    custom_formatters: list[str] | None = None,
    custom_formatters_kwargs: dict[str, Any] | None = None,
    use_pendulum: bool = False,
    http_query_parameters: Sequence[tuple[str, str]] | None = None,
) -> None:
    remote_text_cache: DefaultPutDict[str, str] = DefaultPutDict()
    input_text = None

    kwargs: dict[str, Any] = {}
    from datamodel_code_generator.parser.jsonschema import JsonSchemaParser

    parser_class = JsonSchemaParser

    data_model_types = get_data_model_types(output_model_type, target_python_version)
    parser = parser_class(
        source=input_text or input_,
        data_model_type=data_model_types.data_model,
        data_model_root_type=data_model_types.root_model,
        data_model_field_type=data_model_types.field_model,
        data_type_manager_type=data_model_types.data_type_manager,
        base_class=base_class,
        additional_imports=additional_imports,
        custom_template_dir=custom_template_dir,
        extra_template_data=extra_template_data,
        target_python_version=target_python_version,
        dump_resolve_reference_action=data_model_types.dump_resolve_reference_action,
        validation=validation,
        field_constraints=field_constraints,
        snake_case_field=snake_case_field,
        strip_default_none=strip_default_none,
        aliases=aliases,
        allow_population_by_field_name=allow_population_by_field_name,
        allow_extra_fields=allow_extra_fields,
        apply_default_values_for_required_fields=apply_default_values_for_required_fields,
        force_optional_for_required_fields=force_optional_for_required_fields,
        class_name=class_name,
        use_standard_collections=use_standard_collections,
        base_path=input_.parent if isinstance(input_, Path) and input_.is_file() else None,
        use_schema_description=use_schema_description,
        use_field_description=use_field_description,
        use_default_kwarg=use_default_kwarg,
        reuse_model=reuse_model,
        enum_field_as_literal=LiteralType.All
        if output_model_type == DataModelType.TypingTypedDict
        else enum_field_as_literal,
        use_one_literal_as_default=use_one_literal_as_default,
        set_default_enum_member=True
        if output_model_type == DataModelType.DataclassesDataclass
        else set_default_enum_member,
        use_subclass_enum=use_subclass_enum,
        strict_nullable=strict_nullable,
        use_generic_container_types=use_generic_container_types,
        enable_faux_immutability=enable_faux_immutability,
        remote_text_cache=remote_text_cache,
        disable_appending_item_suffix=disable_appending_item_suffix,
        strict_types=strict_types,
        empty_enum_field_name=empty_enum_field_name,
        custom_class_name_generator=custom_class_name_generator,
        field_extra_keys=field_extra_keys,
        field_include_all_keys=field_include_all_keys,
        field_extra_keys_without_x_prefix=field_extra_keys_without_x_prefix,
        wrap_string_literal=wrap_string_literal,
        use_title_as_name=use_title_as_name,
        use_operation_id_as_name=use_operation_id_as_name,
        use_unique_items_as_set=use_unique_items_as_set,
        http_headers=http_headers,
        http_ignore_tls=http_ignore_tls,
        use_annotated=use_annotated,
        use_non_positive_negative_number_constrained_types=use_non_positive_negative_number_constrained_types,
        original_field_name_delimiter=original_field_name_delimiter,
        use_double_quotes=use_double_quotes,
        use_union_operator=use_union_operator,
        collapse_root_models=collapse_root_models,
        special_field_name_prefix=special_field_name_prefix,
        remove_special_field_name_prefix=remove_special_field_name_prefix,
        capitalise_enum_members=capitalise_enum_members,
        keep_model_order=keep_model_order,
        known_third_party=data_model_types.known_third_party,
        custom_formatters=custom_formatters,
        custom_formatters_kwargs=custom_formatters_kwargs,
        use_pendulum=use_pendulum,
        http_query_parameters=http_query_parameters,
        **kwargs,
    )

    with chdir(output):
        results = parser.parse()
    if not input_filename:
        input_filename = input_.name
    modules = {output: (results, input_filename)}

    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat()

    header = """\
# generated by datamodel-codegen:
#   filename:  {}"""
    if not disable_timestamp:
        header += f"\n#   timestamp: {timestamp}"

    file: IO[Any] | None
    for path, (body, filename) in modules.items():
        file = path.open("wt", encoding=encoding)

        print(custom_file_header or header.format(filename), file=file)
        if body:
            print(file=file)
            print(body.rstrip(), file=file)

        if file is not None:
            file.close()




__all__ = [
    "DefaultPutDict",
    "Error",
    "InputFileType",
    "InvalidClassNameError",
    "LiteralType",
    "PythonVersion",
    "generate",
]
