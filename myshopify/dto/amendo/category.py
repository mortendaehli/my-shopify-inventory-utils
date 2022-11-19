from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class Category(BaseEntity):
    categoryId: Optional[int]
    categoryName: str


class CategoryListResponse(BaseResponse):
    categories: List[Category]
    totalCount: int


class CategoryCreateBody(BaseModel):
    data: List[Category]


class CategoryCreateResponse(BaseModel):
    status: bool
    code: int
    categoryData: List[Category]
    validationMessage: str


class CategorySaveResponse(BaseResponse):
    totalAffected: int
    data: List[CategoryCreateResponse]


class CategoryDetailResponse(BaseResponse):
    data: Category
