from collections import OrderedDict
from typing import Any, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class ProductMetadata(BaseModel):
    name: str
    short_code: str
    brand: str
    sku: Optional[str]
    url: HttpUrl


class ProductImage(BaseModel):
    name: str
    alt: str
    suffix: str
    url: HttpUrl
    image: Any


class ProductDescription(BaseModel):
    name: str
    metadata: Optional[ProductMetadata]
    images: Optional[List[ProductImage]]
    header: str
    summary: str
    features: str
    standard_accessory: str
    detailed_description: str
    optional_accessory: List[ProductMetadata] = Field(default_factory=list)
    technical_specification_dict: OrderedDict
