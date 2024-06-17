from .core import DynamicModel, SchemaParser


def parse_json_schema(schema: dict) -> type[DynamicModel]:
    """
    Parse a JSON schema into a dynamic Pydantic model.

    :param schema: The JSON schema to parse.
    :return: The dynamically created Pydantic model class.
    """
    parser = SchemaParser(schema)
    return parser.parse()
