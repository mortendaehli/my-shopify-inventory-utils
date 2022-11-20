from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class Supplier(BaseEntity):
    supplierId: Optional[int]
    supplierName: str
    address: Optional[str]
    comments: Optional[str]
    companyNumber: Optional[str]
    customerNumber: Optional[str]
    emailAddress: Optional[str]
    location: Optional[str]
    phoneNumber: Optional[str]
    webAddress: Optional[str]
    zip: Optional[str]


class SupplierCreateOrUpdateBody(BaseModel):
    data: List[Supplier]


class SupplierListAllResponse(BaseResponse):
    suppliers: List[Supplier]
    total_count: int


class SupplierCreateOrUpdateResponseData(BaseResponse):
    brandData: Supplier
    validationMessage: List[Any]


class SupplierCreateOrUpdateResponse(BaseResponse):
    data: List[SupplierCreateOrUpdateResponseData]


class SupplierViewDetailsResponse(BaseResponse):
    data: Supplier
