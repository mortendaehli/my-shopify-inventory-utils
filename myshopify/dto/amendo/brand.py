from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, constr

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class Brand(BaseEntity):
    brandId: Optional[int]
    brandName: constr(max_length=90)


class BrandList(BaseResponse):
    brands: List[Brand]
    totalCount: int


class BrandSaveData(BaseModel):
    status: bool
    code: int
    brandData: Brand
    validationMessage: str


class BrandCreateBody(BaseModel):
    data: List[Brand]


class BrandUpdateBody(BaseModel):
    data: List[Brand]


class BrandCreateResponse(BaseResponse):
    data: List[BrandSaveData]


class BrandUpdateResponse(BaseResponse):
    status: bool
    code: int
    dateTimeBeforeQryExec: datetime
    totalAffected: int
    data: [BrandSaveData]


class BrandViewResponse(BaseResponse):
    data: Brand


class BrandIdPathParams(BaseModel):
    brandId: int
