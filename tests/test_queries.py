import pytest
from dynaschema.queries import TypedQueryEngine
from dynaschema.core import DynamicModel


def test_typed_query_engine():
    class ExampleModel(DynamicModel):
        id: str
        createdAt: str

    model_instance = ExampleModel(id="123", createdAt="2023-01-01T00:00:00")
    engine = TypedQueryEngine(ExampleModel)
    result = engine.query("id")
    assert result == "123"
