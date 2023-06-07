"""
Recursively converts a pydantic model into all optional. Useful if you have a FastAPI application where you only want to return a subset of a model, but dont want to create a partial copy of that model.

Example:

```
Class Foo(BaseModel):
  bar: int
  baz: float

Class AllOptionalFoo(Foo, metaclass=AllOptionalMetaclass):
  ...
```
The new class, AllOptionalFoo, now effectivly has the schema of:
```
Class Foo(BaseModel):
  bar: int | None
  baz: float | None
```
"""

from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel
from pydantic.main import ModelMetaclass


class AllOptionalMetaclass(ModelMetaclass):
    def __new__(mcs, name: str, bases: Tuple[type], namespaces: Dict[str, Any], **kwargs):
        annotations: dict = namespaces.get("__annotations__", {})

        for base in bases:
            for base_ in base.__mro__:
                if base_ is BaseModel:
                    break

                annotations.update(base_.__annotations__)

        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]

        namespaces["__annotations__"] = annotations

        return super().__new__(mcs, name, bases, namespaces, **kwargs)
