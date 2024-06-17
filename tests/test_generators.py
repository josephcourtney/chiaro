import pytest
from dynaschema.generators import generate_json_schema
from dynaschema.core import DynamicModel


def test_generate_json_schema():
    class ExampleModel(DynamicModel):
        id: str
        createdAt: str

    schema = generate_json_schema(ExampleModel)
    assert "properties" in schema
    assert "id" in schema["properties"]
    assert "createdAt" in schema["properties"]
