from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class OffsetLimitFromDatePathParams(BaseModel):
    offset: Optional[int]
    limit: Optional[int]
    fromDate: Optional[datetime]


class OffsetLimitFromDateSortOrderPathParams(BaseModel):
    offset: Optional[int]
    limit: Optional[int]
    fromDate: Optional[datetime]
    sortOrder: SortOrder


class OffsetLimitPathParams(BaseModel):
    offset: Optional[int]
    limit: Optional[int]


class IdPathParams(BaseModel):
    Id: Optional[int]


class ProductIdDepartmentIdPathParams(BaseModel):
    product_Id: Optional[int]
    department_Id: Optional[int]


class DepartmentIdPathParams(BaseModel):
    department_Id: Optional[int]


class ProductFilter(BaseModel):
    offset: Optional[int]
    limit: Optional[int]
    filter_lastUpdateDate: str
    filter_productId: Optional[int]
    filter_productName: str
    filter_productNumber: str
    filter_barcode: str
    filter_isActive: float
    filter_isDeleted: float
    filter_isTakeaway: float
    orderBy: str
    sortBy: str
