import logging
from io import BytesIO
from typing import List

import shopify
from PIL import Image

from myshopify import dto

logger = logging.getLogger(__name__)


def _image_to_bytes(image: Image) -> bytes:
    buffered = BytesIO()
    image.save(buffered, format=image.format)
    return buffered.getvalue()


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


def create_product(
    product_dto: dto.shopify.Product,
) -> shopify.Product:
    # Creating the product.
    product = product_dto.to_shopify_object()
    product.save()
    if product.errors:
        raise ValueError(product.errors)

    return product


def create_variant(variant_dto: dto.shopify.ProductVariant) -> shopify.Variant:
    # Creating the product.
    variant = variant_dto.to_shopify_object()
    variant.save()
    if variant.errors:
        raise ValueError(variant.errors)
    return variant


def add_images_to_product(product: shopify.Product, image_list: List[Image.Image]) -> List[shopify.Image]:
    assert product.id is not None
    images = []
    for i, image in enumerate(image_list):
        new_shopify_image = shopify.Image()
        new_shopify_image.product_id = product.id
        new_shopify_image.variant_ids = [variant.id for variant in product.variants]
        new_shopify_image.attach_image(
            data=_image_to_bytes(image), filename=f"{product.title.replace(' ', '_').lower()}_.jpg"
        )
        if new_shopify_image.errors:
            raise ValueError(new_shopify_image.errors)
        new_shopify_image.save()
        images.append(new_shopify_image)
    # product.images = images
    # product.save()
    return images


def update_product(
    product_update_dto: dto.shopify.Product,
) -> shopify.Product:
    assert product_update_dto.id is not None
    product = shopify.Variant.find(id_=product_update_dto.id)
    product_update_dto.to_shopify_object(existing_object=product)
    if product.errors:
        raise ValueError(product.errors)
    product.save()
    return product


def update_variant(
    variant_update_dto: dto.shopify.ProductVariant,
) -> shopify.Variant:
    assert variant_update_dto.id is not None
    variant = shopify.Variant.find(id_=variant_update_dto.id)
    variant_update_dto.to_shopify_object(existing_object=variant)
    if variant.errors:
        raise ValueError(variant.errors)
    variant.save()
    return variant


def update_inventory(inventory_level_dto: dto.shopify.InventoryLevel) -> None:
    assert inventory_level_dto.inventory_item_id is not None
    shopify.InventoryLevel.set(
        location_id=inventory_level_dto.location_id,
        inventory_item_id=inventory_level_dto.inventory_item_id,
        available=inventory_level_dto.available,
    )
