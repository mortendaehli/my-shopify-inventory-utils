from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, conint


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class OffsetLimitFromDatePathParams(BaseModel):
    fromDate: Optional[date] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class OffsetLimitFromDateSortOrderPathParams(BaseModel):
    fromDate: Optional[date] = None
    offset: Optional[int] = None
    limit: Optional[conint(le=50)] = 50
    sortOrder: Optional[SortOrder] = SortOrder.ASC


class OrderStatusLimitOffsetOrderByParams(BaseModel):
    OrderStatus: Optional[int] = None
    limit: Optional[int] = 50
    offset: Optional[int] = None
    orderby: Optional[SortOrder] = SortOrder.ASC


class OffsetLimitPathParams(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None


class IdPathParams(BaseModel):
    id: int


class ProductIdDepartmentIdPathParams(BaseModel):
    productId: int
    departmentId: int


class DepartmentIdPathParams(BaseModel):
    departmentId: int


class ProductFilter(BaseModel):
    fromDate: Optional[date] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    orderBy: Optional[str] = None
    sortBy: Optional[str] = None
    departmentIds: Optional[str] = None


class CategoryIdPathParams(BaseModel):
    categoryId: int


class CustomerIdPathParams(BaseModel):
    customerId: int


class OrderNumberPathParams(BaseModel):
    orderNumber: int


class ProductIdPathParams(BaseModel):
    productId: int


class ProductIdOrderIdPathParams(BaseModel):
    productId: int
    productOrderId: Optional[int]


class SupplierIdPathParams(BaseModel):
    supplierId: int


class VatRateIdPathParams(BaseModel):
    vatRateId: int
