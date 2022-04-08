import logging
from io import BytesIO
from typing import Dict, List, Union
from urllib.error import HTTPError

import shopify
from PIL import Image
from pyactiveresource.connection import ClientError, ServerError
from retry import retry

from myshopify import dto
from myshopify.utils import expand_to_square

logger = logging.getLogger(__name__)


def _image_to_bytes(image: Image, image_format: str) -> bytes:
    buffered = BytesIO()
    image.save(buffered, format=image_format)
    return buffered.getvalue()


def get_all_shopify_resources(resource_type, **kwargs):
    logger.info(f"Reading all resources of type: {type(resource_type)}")
    resource_count = resource_type.count(**kwargs)
    resources = []
    i = 1
    if resource_count > 0:
        page = resource_type.find(**kwargs)
        resources.extend(page)
        while page.has_next_page():
            f"Reading resource page: {i}/{resource_count}"
            page = page.next_page()
            resources.extend(page)
            i += 1
    return resources


def get_number_from_string(x):
    return float(x.__repr__().replace(",", ".").replace(r"\xa0", "").replace("'", ""))


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def create_product(product_dto: dto.shopify.Product) -> shopify.Product:
    logger.info(f"Creating Product: {product_dto.title}")
    product = product_dto.to_shopify_object()
    product.save()
    if product.errors.errors:
        raise ValueError(product.errors.errors)
    return product


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def create_variant(variant_dto: dto.shopify.ProductVariant) -> shopify.Variant:
    logger.info(f"Creating Variant: {variant_dto.title} - sku: {variant_dto.sku}")
    variant = variant_dto.to_shopify_object()
    variant.save()
    if variant.errors.errors:
        raise ValueError(variant.errors.errors)
    return variant


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def add_images_to_product(
    product: shopify.Product, image_list: List[Image.Image], make_square: bool = True, resize: bool = True
) -> List[shopify.Image]:
    """
    Note! We are resizing all images to squares of (2048, 2048).
    """
    logger.info(f"Adding images to Product: {product.title}")
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


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def update_product(product_update_dto: dto.shopify.Product, shopify_product: shopify.Product) -> shopify.Product:
    logger.info(f"Updating Product: {shopify_product.title}")
    assert product_update_dto.id == shopify_product.id
    product = product_update_dto.to_shopify_object(existing_object=shopify_product)
    if product.errors.errors:
        raise ValueError(product.errors.errors)
    product.save()

    return product


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def update_variant(variant_update_dto: dto.shopify.ProductVariant, shopify_variant: shopify.Variant) -> shopify.Variant:
    logger.info(f"Updating Variant sku: {shopify_variant.sku}")
    assert variant_update_dto.id == shopify_variant.id
    variant = variant_update_dto.to_shopify_object(existing_object=shopify_variant)
    if variant.errors.errors:
        raise ValueError(variant.errors.errors)
    variant.save()
    return variant


def add_metafields(product: shopify.Product, metafields_dto: List[dto.shopify.Metafield]) -> None:
    logger.info(f"Adding Product Metafields: {product.title}")
    for metafield_dto in metafields_dto:
        add_metafield(product=product, metafield_dto=metafield_dto)


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def add_metafield(product: shopify.Product, metafield_dto: dto.shopify.Metafield) -> None:
    metafield = metafield_dto.to_shopify_object()
    metafield.save()
    if metafield.errors.errors:
        raise ValueError(metafield.errors.errors)
    product.add_metafield(metafield=metafield)


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def update_inventory(inventory_level_dto: dto.shopify.InventoryLevel) -> None:
    assert inventory_level_dto.inventory_item_id is not None
    shopify.InventoryLevel.set(
        location_id=inventory_level_dto.location_id,
        inventory_item_id=inventory_level_dto.inventory_item_id,
        available=inventory_level_dto.available,
    )


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def delete_variant(variant: shopify.Variant) -> None:
    logger.info(f"Deleting Variant sku: {variant.sku}")
    variant.destroy()


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def delete_product(product: shopify.Product) -> None:
    logger.info(f"Deleting Product: {product.title}")
    product.destroy()


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def delete_metafield(metafield: shopify.Metafield) -> None:
    metafield.destroy()


@retry((HTTPError, ServerError, ClientError), tries=10, delay=10)
def update_product_metafield(
    product: shopify.Product, data: Dict[str, str], delete_missing: bool = False
) -> List[shopify.Metafield]:
    metafields = product.metafields()
    metafields_keys = [field.attributes["key"] for field in metafields]
    for metafield in metafields:
        if metafield.attributes["key"] in data.keys():
            metafield.value = data[metafield.attributes["key"]]
            metafield.save()
        elif delete_missing:
            delete_metafield(metafield=metafield)
    for key, value in data.items():
        if key not in metafields_keys:
            metafield_dto = generate_product_metafield(key=key, value=value, product_id=product.id)
            add_metafield(product=product, metafield_dto=metafield_dto)
    return metafields


def generate_product_metafields(
    data: Dict[str, Union[str, int, float]], product_id: int
) -> List[dto.shopify.Metafield]:
    metafields = list()
    for key, value in data.items():
        if isinstance(value, str):
            dtype = dto.types.ShopifyType.single_line_text_field
            value_type = dto.types.ShopifyValueType.string
        elif isinstance(value, int):
            dtype = dto.types.ShopifyType.number_integer
            value_type = dto.types.ShopifyValueType.integer
        else:
            raise NotImplementedError(f"Datatype {type(value)} has not been implemented for Metafields")
        metafields.append(
            dto.shopify.Metafield(
                owner_id=product_id,
                owner_resource="product",
                key=key,
                namespace="inventory",
                value=value,
                type=dtype,
                value_type=value_type,
            )
        )

    return metafields


def generate_product_metafield(key: str, value: Union[str, int, float], product_id: int) -> dto.shopify.Metafield:
    if isinstance(value, str):
        dtype = dto.types.ShopifyType.single_line_text_field
        value_type = dto.types.ShopifyValueType.string
    elif isinstance(value, int):
        dtype = dto.types.ShopifyType.number_integer
        value_type = dto.types.ShopifyValueType.integer
    else:
        raise NotImplementedError(f"Datatype {type(value)} has not been implemented for Metafields")
    return dto.shopify.Metafield(
        owner_id=product_id,
        owner_resource="product",
        key=key,
        namespace="inventory",
        value=value,
        type=dtype,
        value_type=value_type,
    )
