# `chiaro` Design Document

The `chiaro` package maintains this design document to provide up-to-date information on the design and implementation principles used in its construction.

## Introduction

The `chiaro` package aims to provide a flexible and dynamic framework for handling JSON schemas and their corresponding data models in Python. By leveraging modern Python features and best practices, `chiaro` ensures robust data validation, easy schema generation, and seamless querying of data structures. The primary goals of the package include:

1. **Dynamic Model Creation**: Enable the creation of Pydantic models from JSON schemas at runtime.
2. **Schema Generation**: Provide tools to generate JSON schemas from Python data models, facilitating a round-trip development process.
3. **Type Safety**: Maintain strict type safety across all operations, ensuring data integrity and reliability.
4. **Ease of Use**: Offer a simple and intuitive API for developers to interact with JSON schemas and data models.

## Implementation

`chiaro` is written in modern Python 3.12 with the following features and principles:

### Comprehensive Type Annotations

- Uses `dict`, `list`, `type` instead of `Dict`, `List`, and `Type`, adhering to [PEP 585](https://www.python.org/dev/peps/pep-0585/).
- Employs modern typing syntax like `dict | list` instead of the older `Union[dict, list]` syntax, as per [PEP 604](https://www.python.org/dev/peps/pep-0604/).

### Design Principles

- **Single Responsibility Principle**: Each module or class has a single, well-defined responsibility.
- **High Cohesion and Low Coupling**: Code is organized to have closely related functionality within modules, and minimal dependencies between modules.

### Documentation

- **Docstrings**: Follow [PEP 257](https://www.python.org/dev/peps/pep-0257/) for detailed docstrings on all public classes, methods, and functions.
- **User Guide**: Provide comprehensive usage instructions with examples.
- **API Reference**: Generate using Sphinx or a similar tool.
- **Contribution Guide**: Include guidelines for contributing, including code style, testing, and pull request processes.

### Code Quality

- **Code Style**: Adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) and use tools like `black` and `flake8`.
- **Type Checking**: Use `mypy` for enforcing type checking.
- **Static Analysis**: Employ tools like `pylint` or `pyflakes`.

### Packaging and Distribution

- **Package Metadata**: Ensure `setup.py` or `pyproject.toml` includes all relevant metadata.
- **Dependency Management**: Use `pipenv` or `poetry`.
- **Continuous Integration**: Set up CI with GitHub Actions, Travis CI, or CircleCI.

### Security

- **Review and Update Dependencies**: Regularly update to fix known vulnerabilities.
- **Security Testing**: Include fuzz testing and SAST.

### Performance

- **Profiling**: Use tools like `cProfile` to identify bottlenecks.
- **Caching**: Implement caching strategies where appropriate.

### Version Control

- **Semantic Versioning**: Follow SemVer for versioning.
- **Changelog**: Maintain a changelog for documenting notable changes.

### Configuration Management

- Use tools like `pydantic`'s settings management or `configparser` for handling configuration.

### Testing

- Code is optimized for easy testing with a comprehensive test suite using pytest.

#### Testing Best Practices

- **Fixtures**: Reusable setup code.
- **Parameterization**: Running tests with multiple sets of data.
- **Mocking**: Replacing parts of the system under test with mock objects.
- **Doctests**: Including tests within docstrings to ensure examples in documentation are up-to-date and functional.

#### Test Hierarchy

- **Static Tests**:
  - **Linting**: Checking code against style guidelines and coding standards.
  - **Formatting**: Ensuring code adheres to a consistent style.
  - **Static Analysis**: Analyzing code for potential errors and code smells without executing it.
- **Unit Tests**:
  - Test the expected outputs and side effects of a single function for the full range of inputs.
- **Component Tests**:
  - Test the behavior of a class or module in isolation.
- **Integration Tests**:
  - Test cooperation and coordination of different units and components.
  - Test behavior when interacting with external components.
- **API Tests**:
  - Test API endpoints for functionality, security, and performance under different simulated network conditions.
- **System Tests**:
  - Test the full integrated system.
- **End-to-End Tests**:
  - Simulate an entire workflow as it would be used in practice.
- **Performance Tests**:
  - Test performance under varying conditions and loads to ensure no performance degradation.
- **Smoke Tests**:
  - Broad tests covering high-level functionality.
- **Sanity Tests**:
  - Narrow, detailed tests to confirm that a particular feature works or that a specific bug is no longer present.

#### Testing Techniques

- **Regression Testing**: Ensuring new changes do not break existing features.
- **Security Testing**: Focusing on vulnerabilities and potential exploits.
- **Compatibility Testing**: Ensuring uniform behavior in varied environments and configurations.
- **Exploratory Testing**: Discovering unexpected issues without predefined test cases.
- **Mutation Testing**: Introducing small changes to the code to ensure tests can detect defects.

## Design Patterns

### Singleton Pattern (TypeRegistry)
- **Description**: Ensures there is only one instance managing custom type definitions.
- **Purpose**: Maintains consistency and avoids conflicts in type registrations.

### Factory Method (Dynamic Model Creation)
- **Description**: The `DynamicModel.from_schema` method acts as a factory method to create dynamic model classes from JSON schemas.
- **Purpose**: Encapsulates the logic for model creation and allows flexibility in instantiation.

### Strategy Pattern (Serialization/Deserialization)
- **Description**: Custom types in the `TypeRegistry` are registered with specific serialization and deserialization functions.
- **Purpose**: Allows different serialization/deserialization behaviors to be easily swapped or extended.

### Facade Pattern (SchemaParser and SchemaGenerator)
- **Description**: These classes provide a simplified interface for parsing and generating schemas.
- **Purpose**: Hides the complexity of the underlying processes and provides a cleaner API for users.

### Builder Pattern (Dynamic Model Construction)
- **Description**: Facilitates the construction of dynamic models with a clear, step-by-step approach.
- **Purpose**: Provides more flexibility and readability, especially for complex schemas.

### Decorator Pattern (Validation and Transformation)
- **Description**: Adds validation or transformation logic to model methods using decorators.
- **Purpose**: Enhances model functionality without modifying their structure.

### Command Pattern (Query Execution)
- **Description**: Encapsulates query logic as command objects.
- **Purpose**: Allows for flexible query execution, history, and undo/redo operations.

### Fluent Interface Pattern (Query Construction)
- **Description**: Queries are built with chained methods.
- **Purpose**: Chained queries enable IDE completion, type safety, and high readability. Additionally, it enables optimizations like lazy execution.