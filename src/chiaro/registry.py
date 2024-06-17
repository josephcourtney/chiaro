from collections.abc import Callable


class TypeRegistry:
    """Singleton class to maintain custom type definitions and their serialization/deserialization logic."""

    _instance = None
    _types: dict[str, dict[str, Callable]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register_type(self, type_name: str, serializer: Callable, deserializer: Callable) -> None:
        """
        Register a new custom type with its serializer and deserializer.

        :param type_name: The name of the custom type.
        :param serializer: The function to serialize the custom type.
        :param deserializer: The function to deserialize the custom type.
        """
        self._types[type_name] = {"serializer": serializer, "deserializer": deserializer}

    def get_serializer(self, type_name: str) -> Callable:
        """
        Retrieve the serializer for a given type.

        :param type_name: The name of the custom type.
        :return: The serializer function.
        """
        return self._types[type_name]["serializer"]

    def get_deserializer(self, type_name: str) -> Callable:
        """
        Retrieve the deserializer for a given type.

        :param type_name: The name of the custom type.
        :return: The deserializer function.
        """
        return self._types[type_name]["deserializer"]
