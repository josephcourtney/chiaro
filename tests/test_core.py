import pytest
from dynaschema.core import DynamicModel, SchemaParser, SchemaGenerator


def test_dynamic_model_from_schema():
    schema = {
        "type": "object",
        "properties": {"id": {"type": "string"}, "createdAt": {"type": "string", "format": "date-time"}},
        "required": ["id", "createdAt"],
    }
    model_cls = DynamicModel.from_schema(schema)
    assert hasattr(model_cls, "id")
    assert hasattr(model_cls, "createdAt")
    instance = model_cls(id="123", createdAt="2023-01-01T00:00:00")
    assert instance.id == "123"
    assert instance.createdAt == "2023-01-01T00:00:00"


def test_dynamic_model_to_schema():
    class ExampleModel(DynamicModel):
        id: str
        createdAt: str

    model_instance = ExampleModel(id="123", createdAt="2023-01-01T00:00:00")
    schema = model_instance.to_schema()
    assert "properties" in schema
    assert "id" in schema["properties"]
    assert "createdAt" in schema["properties"]


def test_schema_parser():
    schema = {
        "type": "object",
        "properties": {"id": {"type": "string"}, "createdAt": {"type": "string", "format": "date-time"}},
        "required": ["id", "createdAt"],
    }
    parser = SchemaParser(schema)
    model_cls = parser.parse()
    assert hasattr(model_cls, "id")
    assert hasattr(model_cls, "createdAt")


def test_schema_generator():
    class ExampleModel(DynamicModel):
        id: str
        createdAt: str

    generator = SchemaGenerator(ExampleModel)
    schema = generator.generate()
    assert "properties" in schema
    assert "id" in schema["properties"]
    assert "createdAt" in schema["properties"]
