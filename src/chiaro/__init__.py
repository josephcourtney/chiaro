from .core import DynamicModel, SchemaGenerator, SchemaParser
from .queries import TypedQueryEngine
from .registry import TypeRegistry
from .types import register_custom_types

__version__ = "0.1.0"

__all__ = [
    "DynamicModel",
    "SchemaGenerator",
    "SchemaParser",
    "TypeRegistry",
    "TypedQueryEngine",
    "register_custom_types",
]

# Register custom types on import
register_custom_types()
