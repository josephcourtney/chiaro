import pytest
from dynaschema.parsers import parse_json_schema
from dynaschema.core import DynamicModel


def test_parse_json_schema():
    schema = {
        "type": "object",
        "properties": {"id": {"type": "string"}, "createdAt": {"type": "string", "format": "date-time"}},
        "required": ["id", "createdAt"],
    }
    model_cls = parse_json_schema(schema)
    assert issubclass(model_cls, DynamicModel)
    instance = model_cls(id="123", createdAt="2023-01-01T00:00:00")
    assert instance.id == "123"
    assert instance.createdAt == "2023-01-01T00:00:00"
