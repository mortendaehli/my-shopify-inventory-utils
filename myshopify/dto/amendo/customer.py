from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseEntity, BaseResponse
from myshopify.dto.amendo.category import Category, CategorySaveResponseData


class Customer(BaseEntity):
    customerId: int
    name: str
    address: str
    zip: str
    location: str
    phoneNumber: str
    email: str
    country: str


class CustomerList(BaseResponse):
    data: List[Customer]
    totalCount: int


class CustomerSavePostRequest(BaseModel):
    data: List[Category]


class CustomerSaveResponseData(BaseModel):
    status: bool
    code: int
    customerData: [Customer]
    validationMessage: str


class CustomerSaveResponse(BaseResponse):
    totalAffected: int
    data: [CategorySaveResponseData]


class CustomerIdPathParams(BaseModel):
    customerId: Optional[int]
