from __future__ import annotations

from typing import List

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class Department(BaseEntity):
    departmentId: int
    departmentName: str
    companyName: str
    companyNumber: str
    type: str
    address: str
    zip: str
    location: str
    receiptAddress: str
    receiptZip: str
    receiptLocation: str
    phoneNumber: str
    email: str
    url: str
    photo: str
    departmentImage: str
    departmentImageUrl: str


class DepartmentViewResponse(BaseResponse):
    departmentInfo: List[Department]
    total_count: int
