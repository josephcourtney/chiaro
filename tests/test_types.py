import pytest
from dynaschema.types import register_custom_types
from dynaschema.registry import TypeRegistry


def test_register_custom_types():
    register_custom_types()
    registry = TypeRegistry()
    serializer = registry.get_serializer("DateTime")
    deserializer = registry.get_deserializer("DateTime")
    assert callable(serializer)
    assert callable(deserializer)

    from datetime import datetime

    dt = datetime(2023, 1, 1)
    dt_str = serializer(dt)
    assert dt_str == "2023-01-01T00:00:00"
    dt_obj = deserializer(dt_str)
    assert dt_obj == dt
