from __future__ import annotations

from typing import Any, List, Optional, Union

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class ProductCategory(BaseModel):
    id: int
    name: Optional[str]


class ProductDepartment(BaseEntity):
    departmentId: int
    stockQuantity: Optional[float]
    incPrice: Optional[float]
    takeawayIncPrice: Optional[float]


class Product(BaseEntity):
    productId: Optional[int]
    productName: Optional[str]
    productNumber: Optional[str]
    barcode: Optional[str]
    description: Optional[str]
    departmentId: Optional[int]
    brandId: Optional[int]
    brandName: Optional[str]
    vatRateId: Optional[int]  # Does not seem possible to set by ID?!
    vatRatePercent: Optional[float]
    takeawayVatRateId: Optional[int]
    takeawayVatRatePercent: Optional[float]
    costPrice: Optional[float]
    priceIncVat: Optional[float]
    takeawayPriceIncVat: Optional[float]
    isTakeaway: Optional[bool]
    stockControl: Optional[bool]
    hasVariant: Optional[bool]
    isCombo: Optional[bool]
    hasConnected: Optional[bool]
    childProductsOnReceipt: Optional[bool]
    isOpenPrice: Optional[bool]
    showOnWeb: Optional[bool]
    printOnBong: Optional[bool]
    productUnitId: Optional[int]
    categoryId: Optional[int]
    category: Optional[ProductCategory]
    supplierId: Optional[int]
    supplierName: Optional[str]
    variants: Optional[List[Any]]
    images: Optional[List[Any]]
    departments: Optional[List[ProductDepartment]]


class ProductVariantAttribute(BaseModel):
    """Warning! "-" not "_" """

    variant_group: str
    variant_value: str


class ProductVariant(BaseEntity):
    parentId: int
    productName: Optional[str]
    productNumber: Optional[str]
    barcode: Optional[str]
    showOnWeb: Optional[bool]
    attributes: Optional[List[Union[ProductVariantAttribute, dict]]]
    departments: Optional[List[ProductDepartment]]


class ProductListResponse(BaseResponse):
    data: List[Product]


class ProductCreateOrUpdateRequestBody(BaseModel):
    data: List[Product]


class ProductVariantCreateOrUpdateRequestBody(BaseModel):
    data: List[ProductVariant]


class ProductUpdateByIdRequestBody(BaseModel):
    data: Product


class ProductPostResponseData(BaseResponse):
    productData: Product


class ProductVariantPostResponseData(BaseResponse):
    productData: Product


class ProductPostResponse(BaseResponse):
    data: Optional[List[ProductPostResponseData]]


class ProductVariantPostResponse(BaseResponse):
    data: Optional[List[ProductVariant]]
    validationMessages: List[Any]
    totalAffected: Optional[int]
    totalFailedVariants: Optional[int]


class ProductViewDetailsResponse(BaseResponse):
    data: Product
