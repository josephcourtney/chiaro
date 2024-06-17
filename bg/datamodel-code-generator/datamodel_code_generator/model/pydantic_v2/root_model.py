from __future__ import annotations

from typing import Any, ClassVar

from datamodel_code_generator.model.pydantic_v2.base_model import BaseModel


class RootModel(BaseModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = "pydantic_v2/RootModel.jinja2"
    BASE_CLASS: ClassVar[str] = "pydantic.RootModel"

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        if "custom_base_class" in kwargs:
            kwargs.pop("custom_base_class")

        super().__init__(**kwargs)

    def _get_config_extra(self) -> Literal[allow, forbid] | None:
        return None
