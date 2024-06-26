from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Set,
    Tuple,
    TypeVar,
)
from warnings import warn

from jinja2 import Environment, FileSystemLoader, Template
from pydantic import Field

from datamodel_code_generator.imports import (
    IMPORT_ANNOTATED,
    IMPORT_ANNOTATED_BACKPORT,
    IMPORT_OPTIONAL,
    IMPORT_UNION,
    Import,
)
from datamodel_code_generator.reference import Reference, _BaseModel
from datamodel_code_generator.types import (
    ANY,
    NONE,
    UNION_PREFIX,
    DataType,
    Nullable,
    chain_as_tuple,
    get_optional_type,
)
from datamodel_code_generator.util import ConfigDict, cached_property

TEMPLATE_DIR: Path = Path(__file__).parents[0] / "template"

ALL_MODEL: str = "#all#"

ConstraintsBaseT = TypeVar("ConstraintsBaseT", bound="ConstraintsBase")


class ConstraintsBase(_BaseModel):
    unique_items: bool | None = Field(None, alias="uniqueItems")
    _exclude_fields: ClassVar[set[str]] = {"has_constraints"}
    model_config = ConfigDict(arbitrary_types_allowed=True, ignored_types=(cached_property,))

    @cached_property
    def has_constraints(self) -> bool:
        return any(v is not None for v in self.dict().values())

    @staticmethod
    def merge_constraints(a: ConstraintsBaseT, b: ConstraintsBaseT) -> ConstraintsBaseT | None:
        constraints_class = None
        if isinstance(a, ConstraintsBase):
            root_type_field_constraints = {k: v for k, v in a.dict(by_alias=True).items() if v is not None}
            constraints_class = a.__class__
        else:
            root_type_field_constraints = {}

        if isinstance(b, ConstraintsBase):
            model_field_constraints = {k: v for k, v in b.dict(by_alias=True).items() if v is not None}
            constraints_class = constraints_class or b.__class__
        else:
            model_field_constraints = {}

        if not issubclass(constraints_class, ConstraintsBase):
            return None

        return constraints_class.parse_obj(
            root_type_field_constraints | model_field_constraints
        )


class DataModelFieldBase(_BaseModel):
    name: str | None = None
    default: Any | None = None
    required: bool = False
    alias: str | None = None
    data_type: DataType
    constraints: Any = None
    strip_default_none: bool = False
    nullable: bool | None = None
    parent: Any | None = None
    extras: ClassVar[dict[str, Any]] = {}
    use_annotated: bool = False
    has_default: bool = False
    use_field_description: bool = False
    const: bool = False
    original_name: str | None = None
    use_default_kwarg: bool = False
    use_one_literal_as_default: bool = False
    _exclude_fields: ClassVar[set[str]] = {"parent"}
    _pass_fields: ClassVar[set[str]] = {"parent", "data_type"}
    can_have_extra_keys: ClassVar[bool] = True

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if self.data_type.reference or self.data_type.data_types:
            self.data_type.parent = self
        self.process_const()

    def process_const(self) -> None:
        if "const" not in self.extras:
            return
        self.default = self.extras["const"]
        self.const = True
        self.required = False
        self.nullable = False

    @property
    def type_hint(self) -> str:
        type_hint = self.data_type.type_hint

        if not type_hint:
            return NONE
        if self.has_default_factory or (self.data_type.is_optional and self.data_type.type != ANY):
            return type_hint
        if self.nullable is not None:
            if self.nullable:
                return get_optional_type(type_hint, self.data_type.use_union_operator)
            return type_hint
        if self.required or not self.fall_back_to_nullable:
            return type_hint
        return get_optional_type(type_hint, self.data_type.use_union_operator)

    def imports(self) -> tuple[Import, ...]:
        type_hint = self.type_hint
        has_union = not self.data_type.use_union_operator and UNION_PREFIX in type_hint
        imports: list[tuple[Import] | Iterator[Import]] = [
            (
                i
                for i in self.data_type.all_imports
                if has_union or i != IMPORT_UNION
            )
        ]

        if self.fall_back_to_nullable:
            if (
                self.nullable or (self.nullable is None and not self.required)
            ) and not self.data_type.use_union_operator:
                imports.append((IMPORT_OPTIONAL,))
        elif self.nullable and not self.data_type.use_union_operator:
            imports.append((IMPORT_OPTIONAL,))
        if self.use_annotated and self.annotated:
            import_annotated = (
                IMPORT_ANNOTATED
                if self.data_type.python_version.has_annotated_type
                else IMPORT_ANNOTATED_BACKPORT
            )
            imports.append((import_annotated,))
        return chain_as_tuple(*imports)

    @property
    def docstring(self) -> str | None:
        if self.use_field_description:
            description = self.extras.get("description", None)
            if description is not None:
                return f"{description}"
        return None

    @property
    def unresolved_types(self) -> frozenset[str]:
        return self.data_type.unresolved_types

    @property
    def field(self) -> str | None:
        return None

    @property
    def method(self) -> str | None:
        return None

    @property
    def represented_default(self) -> str:
        return repr(self.default)

    @property
    def annotated(self) -> str | None:
        return None

    @property
    def has_default_factory(self) -> bool:
        return "default_factory" in self.extras

    @property
    def fall_back_to_nullable(self) -> bool:
        return True


@lru_cache()
def get_template(template_file_path: Path) -> Template:
    loader = FileSystemLoader(str(TEMPLATE_DIR / template_file_path.parent))
    environment: Environment = Environment(loader=loader)
    return environment.get_template(template_file_path.name)


def get_module_path(name: str, file_path: Path | None) -> List[str]:
    if file_path:
        return [
            *file_path.parts[:-1],
            file_path.stem,
            *name.split(".")[:-1],
        ]
    return name.split(".")[:-1]


def get_module_name(name: str, file_path: Path | None) -> str:
    return ".".join(get_module_path(name, file_path))


class TemplateBase(ABC):
    @property
    @abstractmethod
    def template_file_path(self) -> Path:
        raise NotImplementedError

    @cached_property
    def template(self) -> Template:
        return get_template(self.template_file_path)

    @abstractmethod
    def render(self) -> str:
        raise NotImplementedError

    def _render(self, *args: Any, **kwargs: Any) -> str:
        return self.template.render(*args, **kwargs)

    def __str__(self) -> str:
        return self.render()


class BaseClassDataType(DataType): ...


UNDEFINED: Any = object()


class DataModel(TemplateBase, Nullable, ABC):
    TEMPLATE_FILE_PATH: ClassVar[str] = ""
    BASE_CLASS: ClassVar[str] = ""
    DEFAULT_IMPORTS: ClassVar[tuple[Import, ...]] = ()

    def __init__(
        self,
        *,
        reference: Reference,
        fields: list[DataModelFieldBase],
        decorators: list[str] | None = None,
        base_classes: list[Reference] | None = None,
        custom_base_class: str | None = None,
        custom_template_dir: Path | None = None,
        extra_template_data: defaultdict[str, Dict[str, Any]] | None = None,
        methods: list[str] | None = None,
        path: Path | None = None,
        description: str | None = None,
        default: Any = UNDEFINED,
        nullable: bool = False,
    ) -> None:
        if not self.TEMPLATE_FILE_PATH:
            msg = "TEMPLATE_FILE_PATH is undefined"
            raise Exception(msg)

        self._custom_template_dir: Path | None = custom_template_dir
        self.decorators: list[str] = decorators or []
        self._additional_imports: list[Import] = []
        self.custom_base_class = custom_base_class
        if base_classes:
            self.base_classes: list[BaseClassDataType] = [
                BaseClassDataType(reference=b) for b in base_classes
            ]
        else:
            self.set_base_class()

        self.file_path: Path | None = path
        self.reference: Reference = reference

        self.reference.source = self

        self.extra_template_data = (
            extra_template_data[self.name] if extra_template_data is not None else defaultdict(dict)
        )

        self.fields = self._validate_fields(fields) if fields else []

        for base_class in self.base_classes:
            if base_class.reference:
                base_class.reference.children.append(self)

        if extra_template_data and (all_model_extra_template_data := extra_template_data.get(ALL_MODEL)):
            self.extra_template_data.update(all_model_extra_template_data)

        self.methods: list[str] = methods or []

        self.description = description
        for field in self.fields:
            field.parent = self

        self._additional_imports.extend(self.DEFAULT_IMPORTS)
        self.default: Any = default
        self._nullable: bool = nullable

    def _validate_fields(self, fields: list[DataModelFieldBase]) -> list[DataModelFieldBase]:
        names: set[str] = set()
        unique_fields: list[DataModelFieldBase] = []
        for field in fields:
            if field.name:
                if field.name in names:
                    warn(f"Field name `{field.name}` is duplicated on {self.name}")
                    continue
                names.add(field.name)
            unique_fields.append(field)
        return unique_fields

    def set_base_class(self) -> None:
        base_class = self.custom_base_class or self.BASE_CLASS
        if not base_class:
            self.base_classes = []
            return
        base_class_import = Import.from_full_path(base_class)
        self._additional_imports.append(base_class_import)
        self.base_classes = [BaseClassDataType.from_import(base_class_import)]

    @cached_property
    def template_file_path(self) -> Path:
        template_file_path = Path(self.TEMPLATE_FILE_PATH)
        if self._custom_template_dir is not None:
            custom_template_file_path = self._custom_template_dir / template_file_path
            if custom_template_file_path.exists():
                return custom_template_file_path
        return template_file_path

    @property
    def imports(self) -> tuple[Import, ...]:
        return chain_as_tuple(
            (i for f in self.fields for i in f.imports),
            self._additional_imports,
        )

    @property
    def reference_classes(self) -> frozenset[str]:
        return frozenset(
            {r.reference.path for r in self.base_classes if r.reference}
            | {t for f in self.fields for t in f.unresolved_types}
        )

    @property
    def name(self) -> str:
        return self.reference.name

    @property
    def duplicate_name(self) -> str:
        return self.reference.duplicate_name or ""

    @property
    def base_class(self) -> str:
        return ", ".join(b.type_hint for b in self.base_classes)

    @staticmethod
    def _get_class_name(name: str) -> str:
        return name.rsplit(".", 1)[-1] if "." in name else name

    @property
    def class_name(self) -> str:
        return self._get_class_name(self.name)

    @class_name.setter
    def class_name(self, class_name: str) -> None:
        if "." in self.reference.name:
            self.reference.name = f"{self.reference.name.rsplit(".", 1)[0]}.{class_name}"
        else:
            self.reference.name = class_name

    @property
    def duplicate_class_name(self) -> str:
        return self._get_class_name(self.duplicate_name)

    @property
    def module_path(self) -> list[str]:
        return get_module_path(self.name, self.file_path)

    @property
    def module_name(self) -> str:
        return get_module_name(self.name, self.file_path)

    @property
    def all_data_types(self) -> Iterator[DataType]:
        for field in self.fields:
            yield from field.data_type.all_data_types
        yield from self.base_classes

    @property
    def nullable(self) -> bool:
        return self._nullable

    @cached_property
    def path(self) -> str:
        return self.reference.path

    def render(self, *, class_name: str | None = None) -> str:
        return self._render(
            class_name=class_name or self.class_name,
            fields=self.fields,
            decorators=self.decorators,
            base_class=self.base_class,
            methods=self.methods,
            description=self.description,
            **self.extra_template_data,
        )
