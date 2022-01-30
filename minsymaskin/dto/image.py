from typing import Any, List

from pydantic import BaseModel, HttpUrl


class ImageListItem(BaseModel):
    file_name: str
    alternative_text: str
    url: HttpUrl
    image: Any


class ImageList(BaseModel):
    images: List[ImageListItem]
