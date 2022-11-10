from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class Category(BaseEntity):
    categoryId: Optional[int]
    categoryName: str


class CategoryListResponse(BaseResponse):
    categories: List[Category]
    total_count: int


class CategorySavePostRequest(BaseModel):
    data: List[Category]


class CategorySaveResponseData(BaseModel):
    status: bool
    code: int
    categoryData: [Category]
    validationMessage: str


class CategorySaveResponse(BaseResponse):
    totalAffected: int
    data: [CategorySaveResponseData]


class CategoryIdPathParams(BaseModel):
    categoryId: Optional[int]


class CategoryDetails(BaseResponse):
    data: Category
