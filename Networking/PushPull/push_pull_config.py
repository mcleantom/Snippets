from typing import Union

from pydantic import BaseModel

__all__ = ["PullConfig"]


class PullConfig(BaseModel):
    protocol: str
    interface: str
    port: Union[str, int]

    @classmethod
    def default(cls):
        return cls(protocol="tcp", interface="127.0.0.1", port="5558")
