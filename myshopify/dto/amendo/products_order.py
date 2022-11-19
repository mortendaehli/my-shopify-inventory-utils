from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseResponse
from myshopify.dto.amendo.department import Department
from myshopify.dto.amendo.supplier import Supplier


class Products(BaseModel):
    product_order_id: int


class ProductsOrderInfoResponse(BaseResponse):
    products: Optional[List[Products]]
    department: Optional[List[Department]]
    supplier: Optional[List[Supplier]]
