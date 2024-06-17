from .core import DynamicModel, SchemaGenerator


def generate_json_schema(model: type[DynamicModel]) -> dict:
    """
    Generate a JSON schema from a Pydantic model.

    :param model: The Pydantic model to generate the schema from.
    :return: The generated JSON schema.
    """
    generator = SchemaGenerator(model)
    return generator.generate()
