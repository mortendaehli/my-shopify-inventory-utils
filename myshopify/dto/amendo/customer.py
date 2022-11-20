from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class Customer(BaseEntity):
    customerId: Optional[int]
    name: str  # Fixme: this is wrong in the documentation. It says CustomerName
    address: Optional[str]
    zip: Optional[str]
    location: Optional[str]
    phoneNumber: Optional[str]
    email: Optional[str]
    country: Optional[str]


class CustomerList(BaseResponse):
    data: List[Customer]
    totalCount: int


class CustomerSavePostRequest(BaseModel):
    data: List[Customer]


class CustomerUpdatePostRequest(BaseModel):
    data: Customer


class CustomerSaveResponseData(BaseModel):
    status: bool
    code: int
    customerData: Customer
    validationMessage: List[Any]


class CustomerSaveResponse(BaseResponse):
    totalAffected: int
    data: List[CustomerSaveResponseData]


class CustomerViewResponse(BaseResponse):
    data: Customer
