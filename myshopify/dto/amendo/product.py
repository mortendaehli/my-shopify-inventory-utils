from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, constr

from myshopify.dto.amendo.base import BaseEntity, BaseResponse
from myshopify.dto.amendo.department import Department


class Product(BaseEntity):
    productId: int
    productName: constr(max_length=150)
    productNumber: constr(max_length=45)
    barcode: constr(max_length=45)
    description: str
    categoryId: int
    brandId: int
    vatRateId: int
    takeawayVatRateId: int
    costPrice: float
    priceIncVat: float
    takeawayPriceIncVat: float
    isTakeaway: bool
    stockControl: bool
    supplierIds: int
    departments: [Department]


class ProductListResponse(BaseResponse):
    data: List[Product]
    totalCount: int


class ProductPostBody(BaseModel):
    data: List[Product]


class ProductIdPathParams(BaseModel):
    productId: Optional[int]
