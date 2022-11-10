from __future__ import annotations
from enum import Enum
from typing import Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

class OffsetLimitFromDatePathParams(BaseModel):
    offset: Optional[int]
    limit: Optional[int]
    fromDate: Optional[datetime]


class Brand(BaseModel):
    brandId: Optional[int]
    brandName: str
    comments: str
    isActive: bool


class BrandSavePostRequest(BaseModel):
    data: Optional[List[Brand]] = None


class BrandIdPathParams(BaseModel):
    brandId: Optional[int]


class OffsetLimitFromDateSortOrderPathParams(BaseModel):
    offset: Optional[int]
    limit: Optional[int]
    fromDate: Optional[datetime]
    sortOrder: SortOrder


class Category(BaseModel):
    categoryId: Optional[int]
    categoryName: str
    isActive: bool


class CategorySavePostRequest(BaseModel):
    data: Optional[List[Category]] = None


class CategoryIdPathParams(BaseModel):
    categoryId: Optional[int]


class OffsetLimitPathParams(BaseModel):
    offset: Optional[int]
    limit: Optional[int]


class CustomerIdPathParams(BaseModel):
    customerId: Optional[int]


class GetaccesstokenPostRequest(BaseModel):
    apikey: str = Field(...,
                        description='Enter api key',
                        example='9sR16Trz7xD718GyIM8NuaPXj2HEFZY')
    password: str = Field(...,
                          description='Enter password',
                          example='test123!')
    username: str = Field(..., description='Enter username', example='apiuser')


class OrderNumberPathParams(BaseModel):
    orderNumber: int


class IdPathParams(BaseModel):
    Id: Optional[int]


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


class ProductIdPathParams(BaseModel):
    productId: Optional[int]


class Data(BaseModel):
    adjust_stock_quantity: Optional[float] = None
    department_id: Optional[float] = None
    product_id: Optional[float] = None


class StockAdjustPostRequest(BaseModel):
    data: Optional[Data] = None


class ProductIdDepartmentIdPathParams(BaseModel):
    product_Id: Optional[int]
    department_Id: Optional[int]


class Data1(BaseModel):
    department_id: Optional[float] = None
    product_id: Optional[float] = None
    stock_quantity: Optional[float] = None


class StockSetPostRequest(BaseModel):
    data: Optional[Data1] = None


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


class VATRate(BaseModel):
    isActive: bool
    vatRatePercent: float


class VatrateSavePostRequest(BaseModel):
    data: Optional[List[VATRate]] = None


class Datum4(BaseModel):
    isActive: bool
    vatRateId: Optional[int]
    vatRatePercent: float


class VatrateSavePutRequest(BaseModel):
    data: Optional[List[Datum4]] = None


class VatRateIdPathParams(BaseModel):
    vatRateId: Optional[int]
