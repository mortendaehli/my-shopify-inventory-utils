from __future__ import annotations

from typing import Any, List, Optional, Union

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class Category(BaseEntity):
    categoryId: Optional[int]
    categoryName: str


class CategoryListResponse(BaseResponse):
    categories: List[Category]
    total_count: Optional[int]


class CategoryCreateBody(BaseModel):
    data: List[Category]


class CategoryCreateResponse(BaseModel):
    status: bool
    code: int
    categoryData: Union[Category, List[Category]]
    validationMessage: List[Any]


class CategorySaveResponse(BaseResponse):
    totalAffected: int
    data: List[CategoryCreateResponse]


class CategoryDetailResponse(BaseResponse):
    data: Category
