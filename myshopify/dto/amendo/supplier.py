from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Supplier(BaseModel):
    address: Any
    comments: Any
    companyNumber: str
    customerNumber: Any
    emailAddress: str
    isActive: bool
    location: Any
    phoneNumber: float
    supplierId: Optional[int]
    supplierName: str
    webAddress: Any
    zip: Any


class SupplierSavePostRequest(BaseModel):
    data: Optional[List[Supplier]] = None


class SupplierIdPathParams(BaseModel):
    supplierId: Optional[int]
