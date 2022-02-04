import logging

import shopify

from myshopify import dto
from typing import Optional, List

logger = logging.getLogger(__name__)


def get_all_shopify_resources(resource_type, **kwargs):
    resource_count = resource_type.count(**kwargs)
    resources = []
    if resource_count > 0:
        page = resource_type.find(**kwargs)
        resources.extend(page)
        while page.has_next_page():
            page = page.next_page()
            resources.extend(page)
    return resources


def get_number_from_string(x):
    return float(x.__repr__().replace(",", ".").replace(r"\xa0", "").replace("'", ""))


def create_product_with_single_variant(
        new_product: dto.shopify.Product,
        new_variant: dto.shopify.ProductVariant,
        images: Optional[List[dto.shopify.ProductImage]]
):
    # Creating the product.
    new_shopify_product = shopify.Product()
    new_shopify_product.title = new_product.title
    new_shopify_product.vendor = new_product.vendor
    new_shopify_product.product_type = new_product.product_type
    new_shopify_product.inventory_quantity = new_product.inventory_quantity
    new_shopify_product.save()

    # Then creating the (only) variant and saving....
    new_shopify_variant = shopify.Variant()
    new_shopify_variant.position = new_variant.position
    new_shopify_variant.sku = new_variant.sku
    new_shopify_variant.price = new_variant.price
    new_shopify_variant.inventory_quantity = new_variant.inventory_quantity
    new_shopify_variant.inventory_policy = new_variant.inventory_policy
    new_shopify_variant.inventory_management = new_variant.inventory_management
    new_shopify_variant.fulfillment_service = new_variant.fulfillment_service

    new_shopify_product.variants = [new_shopify_variant]
    new_shopify_product.save()

    v = new_shopify_product.variants[0]  # We only have 1 variant atm. So we don't vare about other variants

    inventory_level_update = dto.shopify.InventoryLevel(
        inventory_item_id=new_shopify_variant.inventory_item_id,
        location_id=v.id,
        available=new_shopify_variant.inventory_quantity,
    )

    shopify.InventoryLevel.set(
        location_id=inventory_level_update.location_id,
        inventory_item_id=inventory_level_update.inventory_item_id,
        available=inventory_level_update.available,
    )


def update_variant(
    variant: shopify.Variant,
    variant_update: dto.shopify.ProductVariant,
    inventory_level_update: dto.shopify.InventoryLevel,
) -> None:
    
    variant.price = variant_update.price
    variant.option = variant_update.option
    variant.inventory_policy = variant_update.inventory_policy

    shopify.InventoryLevel.set(
        location_id=inventory_level_update.location_id,
        inventory_item_id=inventory_level_update.inventory_item_id,
        available=inventory_level_update.available,
    )
    variant.save()
