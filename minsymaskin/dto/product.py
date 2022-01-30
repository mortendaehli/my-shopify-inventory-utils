from collections import OrderedDict
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class ProductListItem(BaseModel):
    title: str
    product_code: str
    sku: Optional[str]
    url: HttpUrl


class ProductList(BaseModel):
    products: List[ProductListItem]


class Product(BaseModel):
    name: str
    sku: Optional[str] = None
    brand: str
    header: str
    summary: str
    features_header: Optional[str]  # Egenskaper
    features: List[str]
    standard_accessory_header: Optional[str]  # Standard tilbehør
    standard_accessory: List[str]
    detailed_description_header: Optional[str]  # Bli bedre kjent med {name}
    detailed_description: str
    optional_accessory_header: Optional[str]  # Valgfritt tilbehør
    optional_accessory: List[str]
    technical_specification_header: Optional[str]  # Tekniske egenskaper
    technical_specification_dict: OrderedDict
