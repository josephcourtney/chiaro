from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Callable, Dict, TypeVar

import pydantic
from packaging import version
from pydantic import BaseModel as _BaseModel

PYDANTIC_VERSION = version.parse(
    pydantic.VERSION if isinstance(pydantic.VERSION, str) else str(pydantic.VERSION)
)


from typing import Protocol
from typing import runtime_checkable
from yaml import CSafeLoader as SafeLoader

from functools import cached_property


try:
    import tomllib

    def load_toml(path: Path) -> Dict[str, Any]:
        with path.open("rb") as f:
            return tomllib.load(f)

except ImportError:
    import toml

    def load_toml(path: Path) -> Dict[str, Any]:
        return toml.load(path)


SafeLoaderTemp = copy.deepcopy(SafeLoader)
SafeLoaderTemp.yaml_constructors = copy.deepcopy(SafeLoader.yaml_constructors)
SafeLoaderTemp.add_constructor(
    "tag:yaml.org,2002:timestamp",
    SafeLoaderTemp.yaml_constructors["tag:yaml.org,2002:str"],
)
SafeLoader = SafeLoaderTemp

Model = TypeVar("Model", bound=_BaseModel)


def model_validator(
    mode: Literal["before", "after"] = "after",
) -> Callable[[Callable[[Model, Any], Any]], Callable[[Model, Any], Any]]:
    def inner(method: Callable[[Model, Any], Any]) -> Callable[[Model, Any], Any]:
        from pydantic import model_validator as model_validator_v2

        return model_validator_v2(mode=mode)(method)

    return inner


def field_validator(
    field_name: str,
    *fields: str,
    mode: Literal["before", "after"] = "after",
) -> Callable[[Any], Callable[[Model, Any], Any]]:
    def inner(method: Callable[[Model, Any], Any]) -> Callable[[Model, Any], Any]:
        from pydantic import field_validator as field_validator_v2

        return field_validator_v2(field_name, *fields, mode=mode)(method)

    return inner


from pydantic import ConfigDict as ConfigDict


class BaseModel(_BaseModel):
    model_config = ConfigDict(strict=False)
