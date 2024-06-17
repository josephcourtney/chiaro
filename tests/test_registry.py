import pytest
from dynaschema.registry import TypeRegistry


def test_type_registry():
    registry = TypeRegistry()

    def dummy_serializer(value):
        return str(value)

    def dummy_deserializer(value):
        return int(value)

    registry.register_type("DummyType", dummy_serializer, dummy_deserializer)

    serializer = registry.get_serializer("DummyType")
    deserializer = registry.get_deserializer("DummyType")
    assert callable(serializer)
    assert callable(deserializer)

    value = 123
    serialized_value = serializer(value)
    assert serialized_value == "123"
    deserialized_value = deserializer(serialized_value)
    assert deserialized_value == 123
