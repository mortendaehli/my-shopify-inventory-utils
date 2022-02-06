from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

import shopify
from pydantic import BaseModel

from myshopify.dto.types import (
    ShopifyFulfillmentService,
    ShopifyInventoryManagement,
    ShopifyInventoryPolicy,
    ShopifyProductStatus,
    ShopifyPublishScope,
    ShopifyWeightUnit,
)


class ProductVariant(BaseModel):
    # Read only
    id: Optional[int] = None  # Read-only
    title: Optional[str] = None  # Read-only
    presentment_prices: Optional[Dict[str, List[dict]]] = None
    inventory_quantity: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    product_id: Optional[int]
    sku: str
    price: float
    inventory_policy: ShopifyInventoryPolicy
    inventory_management: ShopifyInventoryManagement = ShopifyInventoryManagement.SHOPIFY.value
    fulfillment_service: ShopifyFulfillmentService = ShopifyFulfillmentService.MANUAL.value

    # Optional / Not implemented
    position: Optional[int] = None  # Normally 1 unless we have multiple variants.
    barcode: Optional[str] = None
    compare_at_price: Optional[float] = None
    grams: Optional[int] = None
    image_id: Optional[int] = None
    inventory_item_id: Optional[int] = None
    option: Optional[Dict[str, str]] = None  # {"option1": "Default Title"}
    taxable: Optional[bool] = None
    tax_code: Optional[str] = None
    weight: Optional[int] = None
    weight_unit: Optional[ShopifyWeightUnit] = None

    def to_shopify_object(self, existing_object: Optional[shopify.Variant] = None) -> shopify.Variant:
        if existing_object:
            obj = existing_object
        else:
            obj = shopify.Variant()
        for field in self.__fields__:
            if self.__getattribute__(field) is not None:
                obj.__setattr__(field, self.__getattribute__(field))
        return obj

    @classmethod
    def from_shopify_object(cls, shopify_obj: shopify.Variant):
        data = {}
        for field in cls.fields:
            data[field] = shopify_obj.__getattribute__(field)
        return cls(**data)

    class Config:
        use_enum_values = True


class ProductImage(BaseModel):
    # Read-only
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    data: Optional[Any]

    # Optional / Not implemented
    position: Optional[int] = None
    product_id: Optional[int] = None
    variant_id: Optional[List[int]] = None
    src: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

    def to_shopify_object(self, existing_object: Optional[shopify.Image] = None) -> shopify.Image:
        if existing_object:
            obj = existing_object
        else:
            obj = shopify.Image()
        for field in self.__fields__:
            if self.__getattribute__(field) is not None:
                obj.__setattr__(field, self.__getattribute__(field))
        return obj

    @classmethod
    def from_shopify_object(cls, shopify_obj: shopify.Image):
        data = {}
        for field in cls.__fields__:
            data[field] = shopify_obj.__getattribute__(field)
        return cls(**data)

    class Config:
        use_enum_values = True


class Product(BaseModel):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product#resource_object
    """

    # Read-only
    id: Optional[int]  # Read-only
    created_at: Optional[str] = None  # Read-only
    published_at: Optional[str] = None  # Read-oly
    updated_at: Optional[str] = None  # Read-only

    title: str
    body_html: Optional[str]
    images: Optional[List[Any]]
    options: Optional[Dict[str, Any]]
    product_type: str
    status: ShopifyProductStatus
    tags: Optional[str]  # string "array" with comma
    vendor: Optional[str]
    variants: Optional[List[ProductVariant]] = None

    # Optional / Not implemented
    published_scope: Optional[ShopifyPublishScope] = ShopifyPublishScope.GLOBAL
    template_suffix: Optional[str] = None  # See docs.

    def to_shopify_object(self, existing_object: Optional[shopify.Product] = None) -> shopify.Product:
        if existing_object:
            obj = existing_object
        else:
            obj = shopify.Product()
        for field in self.__fields__:
            if self.__getattribute__(field) is not None:
                obj.__setattr__(field, self.__getattribute__(field))
        return obj

    @classmethod
    def from_shopify_object(cls, shopify_obj: shopify.Product):
        data = {}
        for field in cls.__fields__:
            data[field] = shopify_obj.__getattribute__(field)
        return cls(**data)

    class Config:
        use_enum_values = True
