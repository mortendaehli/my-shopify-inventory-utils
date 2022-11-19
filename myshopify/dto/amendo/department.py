from __future__ import annotations

from typing import List, Optional

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class Department(BaseEntity):
    departmentId: int
    departmentName: str
    departmentNumber: int
    companyName: Optional[str]
    companyNumber: Optional[str]
    type: Optional[str]
    address: Optional[str]
    zip: Optional[str]
    location: Optional[str]
    receiptAddress: Optional[str]
    receiptZip: Optional[str]
    receiptLocation: Optional[str]
    phoneNumber: Optional[str]
    email: Optional[str]
    url: Optional[str]
    photo: Optional[str]
    departmentImage: Optional[str]
    departmentImageUrl: Optional[str]


class DepartmentViewResponse(BaseResponse):
    departmentInfo: Department


class DepartmentListResponse(BaseResponse):
    departments: List[Department]
    totalCount: int
