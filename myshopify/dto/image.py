from typing import Any

from pydantic import BaseModel, HttpUrl


class Image(BaseModel):
    name: str
    alt: str
    suffix: str
    url: HttpUrl
    image: Any
