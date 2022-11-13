from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class OffsetLimitFromDatePathParams(BaseModel):
    offset: int
    limit: int
    from_date: str


class OffsetLimitFromDateSortOrderPathParams(BaseModel):
    offset: int
    limit: int
    from_date: str
    sort_order: SortOrder


class OffsetLimitPathParams(BaseModel):
    offset: int
    limit: int


class IdPathParams(BaseModel):
    Id: int


class ProductIdDepartmentIdPathParams(BaseModel):
    product_Id: int
    department_Id: int


class DepartmentIdPathParams(BaseModel):
    department_Id: int


class ProductFilter(BaseModel):
    offset: int
    limit: int
    filter_lastUpdateDate: str
    filter_productId: int
    filter_productName: str
    filter_productNumber: str
    filter_barcode: str
    filter_isActive: bool
    filter_isDeleted: bool
    filter_isTakeaway: bool
    order_by: str
    sort_by: str
