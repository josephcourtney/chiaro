# `chiaro`

`chiaro` is a flexible and dynamic framework for handling JSON schemas and their corresponding data models in Python. It leverages modern Python features and best practices to ensure robust data validation, easy schema generation, and seamless querying of data structures.

## Features

- **Dynamic Model Creation**: Create Pydantic models from JSON schemas at runtime.
- **Schema Generation**: Generate JSON schemas from Python data models.
- **Type Safety**: Maintain strict type safety across all operations.
- **Ease of Use**: Simple and intuitive API for interacting with JSON schemas and data models.
- **Comprehensive Testing**: Thorough testing strategies to ensure reliability and security.

## Installation

You can install `chiaro` using pip:

```sh
pip install chiaro
```

## Quick Start

### Dynamic Model Creation

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

### Schema Generation

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

### Type-Safe Querying

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

## Documentation

For comprehensive usage instructions and API reference, please refer to the [documentation](https://github.com/yourusername/chiaro).

## Contributing

We welcome contributions to `chiaro`. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a Pull Request.

Please ensure your code follows the project coding standards and includes appropriate tests.

## Testing

Run tests using pytest:

```sh
pytest
```

## License

`chiaro` is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions or issues, please open an issue on GitHub or contact the maintainers.