from datetime import datetime

from .registry import TypeRegistry


class CustomType:
    """Base class for custom types."""


def register_custom_types():
    """Register custom types with the TypeRegistry."""

    # Example registration of a custom type
    def datetime_serializer(dt):
        return dt.isoformat()

    def datetime_deserializer(dt_str):
        return datetime.fromisoformat(dt_str)

    registry = TypeRegistry()
    registry.register_type("DateTime", datetime_serializer, datetime_deserializer)
