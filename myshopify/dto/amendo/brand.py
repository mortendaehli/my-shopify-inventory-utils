from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .base import ResponseBase


class Brand(BaseModel):
    brandId: Optional[int]
    brandName: str
    comments: str
    isActive: Optional[bool]
    isDeleted: Optional[bool]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class BrandsResponse(ResponseBase):
    brands: List[Brand]
    total_count: int


class BrandDetailResponse(BaseModel):
    data: Brand
