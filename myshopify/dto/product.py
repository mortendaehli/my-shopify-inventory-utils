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
    metadata: Optional[ProductMetadata] = None
    images: Optional[List[ProductImage]]
    header: str
    summary: str
    features_header: Optional[str]  # Egenskaper
    features: List[str]
    standard_accessory_header: Optional[str]  # Standard tilbehør
    standard_accessory: List[str]
    detailed_description_header: Optional[str]  # Bli bedre kjent med {name}
    detailed_description: str
    optional_accessory_header: Optional[str]  # Valgfritt tilbehør
    optional_accessory: List[ProductMetadata] = Field(default_factory=list)
    technical_specification_header: Optional[str]  # Tekniske egenskaper
    technical_specification_dict: OrderedDict
