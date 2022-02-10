import logging
from io import BytesIO
from typing import List, Union
from urllib.error import HTTPError

import shopify
from PIL import Image
from pyactiveresource.connection import ServerError
from retry import retry

from myshopify import dto
from myshopify.utils import expand_to_square

logger = logging.getLogger(__name__)


def _image_to_bytes(image: Image, image_format: str) -> bytes:
    buffered = BytesIO()
    image.save(buffered, format=image_format)
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


@retry((HTTPError, ServerError), tries=100, delay=5)
def create_product(product_dto: dto.shopify.Product) -> shopify.Product:
    # Creating the product.
    product = product_dto.to_shopify_object()
    product.save()
    if product.errors.errors:
        raise ValueError(product.errors.errors)
    return product


@retry((HTTPError, ServerError), tries=100, delay=5)
def create_variant(variant_dto: dto.shopify.ProductVariant) -> shopify.Variant:
    # Creating the product.
    variant = variant_dto.to_shopify_object()
    variant.save()
    if variant.errors.errors:
        raise ValueError(variant.errors.errors)
    return variant


@retry((HTTPError, ServerError), tries=100, delay=5)
def add_images_to_product(
    product: shopify.Product, image_list: List[Image.Image], make_square: bool = True, resize: bool = True
) -> List[shopify.Image]:
    """
    Note! We are resizing all images to squares of (2048, 2048).
    """
    assert product.id is not None
    images = []
    for i, image in enumerate(image_list):
        image_format = image.format
        new_shopify_image = shopify.Image()
        new_shopify_image.product_id = product.id
        new_shopify_image.variant_ids = [variant.id for variant in product.variants]
        if make_square:
            image = expand_to_square(image)
        if resize:
            image = image.resize((2048, 2048))
        new_shopify_image.attach_image(
            data=_image_to_bytes(image, image_format=image_format),
            filename=f"{product.title.replace(' ', '_').lower()}_.{image_format.lower()}",
        )
        if new_shopify_image.errors.errors:
            raise ValueError(new_shopify_image.errors.errors)
        new_shopify_image.save()
        images.append(new_shopify_image)
    return images


@retry((HTTPError, ServerError), tries=100, delay=5)
def update_product(product_update_dto: dto.shopify.Product) -> shopify.Product:
    assert product_update_dto.id is not None
    product: shopify.Product = shopify.Product.find(id_=product_update_dto.id)
    product_update_dto.to_shopify_object(existing_object=product)
    if product.errors.errors:
        raise ValueError(product.errors.errors)
    product.save()

    return product


@retry((HTTPError, ServerError), tries=100, delay=5)
def update_variant(variant_update_dto: dto.shopify.ProductVariant) -> shopify.Variant:
    assert variant_update_dto.id is not None
    variant: shopify.Variant = shopify.Variant.find(id_=variant_update_dto.id)
    variant_update_dto.to_shopify_object(existing_object=variant)
    if variant.errors.errors:
        raise ValueError(variant.errors.errors)
    variant.save()
    return variant


@retry((HTTPError, ServerError), tries=100, delay=5)
def add_metafields(
    metafields_dto: List[dto.shopify.Metafield], resource: Union[shopify.Product, shopify.Variant]
) -> None:
    for metafield_dto in metafields_dto:
        metafield = metafield_dto.to_shopify_object()
        metafield.save()
        if metafield.errors.errors:
            raise ValueError(metafield.errors.errors)
        resource.add_metafield(metafield=metafield)


@retry((HTTPError, ServerError), tries=100, delay=5)
def update_inventory(inventory_level_dto: dto.shopify.InventoryLevel) -> None:
    assert inventory_level_dto.inventory_item_id is not None
    shopify.InventoryLevel.set(
        location_id=inventory_level_dto.location_id,
        inventory_item_id=inventory_level_dto.inventory_item_id,
        available=inventory_level_dto.available,
    )


@retry((HTTPError, ServerError), tries=100, delay=5)
def delete_variant(variant: shopify.Variant) -> None:
    variant.destroy()


@retry((HTTPError, ServerError), tries=100, delay=5)
def delete_product(product: shopify.Product) -> None:
    product.destroy()
