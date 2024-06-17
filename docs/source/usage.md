# Usage

This section provides examples and usage instructions for `chiaro`.

## Dynamic Model Creation

Create a Pydantic model from a JSON schema:

```python
from chiaro.core import DynamicModel

schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "age": {"type": "integer"},
    },
    "required": ["id", "name"]
}

MyModel = DynamicModel.from_schema(schema)
model_instance = MyModel(id="123", name="John Doe", age=30)
print(model_instance)
```

## Schema Generation

Generate a JSON schema from a Pydantic model:

```python
from chiaro.core import SchemaGenerator, DynamicModel

class User(DynamicModel):
    id: str
    name: str
    age: int

schema = SchemaGenerator(User).generate()
print(schema)
```

## Type-Safe Querying

Execute type-safe queries on models:

```python
from chiaro.queries import TypedQueryEngine
from chiaro.core import DynamicModel

class User(DynamicModel):
    id: str
    name: str
    age: int

query_engine = TypedQueryEngine(User)
results = (
    query_engine
    .select("id", "name")
    .where("age > 18")
    .order_by("name")
    .limit(5)
    .execute()
)
print(results)
```