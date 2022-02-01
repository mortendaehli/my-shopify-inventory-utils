from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from myshopify.dto.types import (
    ShopifyFulfillmentService,
    ShopifyInventoryManagement,
    ShopifyInventoryPolicy,
    ShopifyProductStatus,
    ShopifyWeightUnit,
)


class Product(BaseModel):
    """
    https://shopify.dev/api/admin-rest/2022-01/resources/product#resource_object
    """

    body_html: Optional[str] = None
    created_at: Optional[str] = None  # Read-only
    handle: Optional[str] = None  # None, otherwise set automatically.
    id: Optional[int] = None  # Read-only
    images: Optional[List[Dict[str, Any]]] = None
    options: Optional[Dict[str, Any]] = None
    product_type: str
    published_at: Optional[str] = None  # See docs.
    published_scope: Optional[str] = None
    status: ShopifyProductStatus
    tags: Optional[str] = None  # See docs.
    template_suffix: Optional[str] = None  # See docs.
    title: str
    updated_at: Optional[str] = None
    variants: Optional[List[ProductVariant]] = None
    vendor: Optional[str] = None

    # Optional
    inventory_quantity: Optional[int] = None


class ProductVariant(BaseModel):
    product_id: Optional[int]
    sku: str
    price: float
    inventory_policy: ShopifyInventoryPolicy
    inventory_management: ShopifyInventoryManagement = ShopifyInventoryManagement.SHOPIFY
    fulfillment_service: ShopifyFulfillmentService = ShopifyFulfillmentService.MANUAL

    # Read only
    id: Optional[int] = None  # Read-only
    title: Optional[str] = None  # Read-only
    presentment_prices: Optional[Dict[str, List[dict]]] = None
    position: Optional[int] = None  # Normally 1 unless we have multiple variants.
    inventory_quantity: Optional[int] = None

    # Optional when creating a new variant
    barcode: Optional[str] = None
    compare_at_price: Optional[float] = None
    created_at: Optional[datetime] = None
    grams: Optional[int] = None
    image_id: Optional[int] = None
    inventory_item_id: Optional[int] = None
    option: Optional[Dict[str, str]] = {"option1": "Default Title"}
    taxable: Optional[bool] = None
    tax_code: Optional[str] = None
    updated_at: Optional[datetime] = None
    weight: Optional[int] = None
    weight_unit: Optional[ShopifyWeightUnit] = None
