import io
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import sleep
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
import shopify
from dotenv import load_dotenv
from PIL import Image
from pydantic import BaseSettings

import myshopify
from myshopify import dto
from myshopify.dto.types import (
    ShopifyFulfillmentService,
    ShopifyInventoryManagement,
    ShopifyInventoryPolicy,
    ShopifyProductStatus,
)
from myshopify.shopify.inventory import (
    add_images_to_product,
    add_metafields,
    create_product,
    create_variant,
    delete_product,
    delete_variant,
    generate_product_metafields,
    get_all_shopify_resources,
    update_inventory,
    update_product,
    update_product_metafield,
    update_variant,
)

load_dotenv()

logging.getLogger("pyactiveresource").setLevel("WARNING")
logging.getLogger("PIL").setLevel("WARNING")
logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    delete_all: bool = False
    delete_old_products: bool = False
    delete_old_metadata: bool = True
    add_metadata: bool = True
    update_metadata: bool = True
    shopify_key: str = os.getenv("MINSYMASKIN_SHOPIFY_KEY")
    shopify_password: str = os.getenv("MINSYMASKIN_SHOPIFY_PWD")
    shopify_shop_name: str = os.getenv("MINSYMASKIN_SHOPIFY_NAME")
    new_product_status: ShopifyProductStatus = ShopifyProductStatus.DRAFT
    allowed_product_categories: Optional[list[str]] = None
    allowed_product_group1: Optional[List[str]] = [
        "Bekledningstoff",
        "Bekledningsmønster",
        "Glidelås",
        "Merkepenn",
        "Linjal",
        "Sakser",
        "Nåler",
        "skjærekniver",
        "skjærematter",
        "Vesketilbehør",
        "Lampe",
        "Strykejern",
        "Diverse",
        "Symaskintilbehør",
        "Symaskiner",
        "Broderigarn",
        "Tråd",
    ]


def _get_metafield_data(row: pd.Series) -> Dict[str, Union[str, int]]:
    data = {
        "price_unit": row["price_unit"],
        "minimum_order_quantity": 3 if row["price_unit"] == "desimeter" else 0,
        "product_category": None if not row["product_category"] else row["product_category"],
        "product_group1": None if not row["product_group1"] else row["product_group1"],
        "product_group2": None if not row["product_group2"] else row["product_group2"],
        "product_group3": None if not row["product_group3"] else row["product_group3"],
        "product_color": None if not row["product_color"] else row["product_color"],
        "fabric_material": None if not row["fabric_material"] else row["fabric_material"],
        "fabric_type": None if not row["fabric_type"] else row["fabric_type"],
        "pattern_type": None if not row["pattern_type"] else row["pattern_type"],  # Fixme: Add to filtering
        "vendor": None if not row["vendor"] else row["vendor"],
        "designer": None if not row["designer"] else row["designer"],
    }
    return {k: v for (k, v) in data.items() if v is not None}


if __name__ == "__main__":
    settings = Settings()

    df = pd.read_pickle(Path(myshopify.__file__).parent.parent / "data" / "shopify_products_export.pickle")
    df = df.groupby("source_id").last()

    if settings.allowed_product_categories is not None:
        df = df.loc[df["product_category"].map(lambda x: x in settings.allowed_product_categories)]
    if settings.allowed_product_group1 is not None:
        df = df.loc[df["product_group1"].map(lambda x: x in settings.allowed_product_group1)]

    shop_url = (
        f"https://{settings.shopify_key}:{settings.shopify_password}"
        f"@{settings.shopify_shop_name}.myshopify.com/admin"
    )

    shopify.ShopifyResource.set_site(value=shop_url)  # noqa

    if settings.delete_all:
        products = get_all_shopify_resources(shopify.Product)
        variants = get_all_shopify_resources(shopify.Variant)
        for variant in variants:
            logger.info(f"Deleting Variant: {variant.title} - sku: {variant.sku}")
            delete_variant(variant=variant)
            sleep(0.25)
        for product in products:
            logger.info(f"Deleting Product: {product.title}")
            delete_product(product=product)
            sleep(0.25)

    # shop = shopify.Shop.current
    products = get_all_shopify_resources(shopify.Product)
    location = shopify.Location.find_first()

    # Clean up old products
    if settings.delete_old_products:
        logger.info("Updating products")
        for i, product in enumerate(products):
            if product.variants[0].sku not in df["sku"].values:
                logger.warning(f"Deleting old product: {product.title} - sku: {product.variants[0].sku}")
                for variant in product.variants:
                    delete_variant(variant=variant)
                delete_product(product=product)

    skus = []
    logger.info("Updating products")
    for i, product in enumerate(products):
        if product.variants[0].sku in df["sku"].values:
            product_row = df.loc[df["sku"] == product.variants[0].sku].iloc[0]

            product_dto = dto.shopify.Product(
                id=product.id,
                product_type=product_row["product_category"],
                tags=product_row["tags"].strip(","),
                vendor=product_row["vendor"],
            )
            update_product(product_update_dto=product_dto, shopify_product=product)

            if product.images is None or product.images == []:
                images = add_images_to_product(
                    product=product,
                    image_list=[Image.open(io.BytesIO(product_row.images))] if product_row.images else []
                )

            if settings.update_metadata:
                metafields_data = _get_metafield_data(row=product_row)
                update_product_metafield(product=product, data=metafields_data, delete_missing=settings.delete_old_metadata)
                sleep(0.5)

            for variant in product.variants:
                skus.append(variant.sku)
                if variant.sku in df["sku"].values:
                    # We are only updating a few fields since we want to keep description text, images, etc.

                    inventory_policy = (
                        ShopifyInventoryPolicy.DENY
                        if bool(product_row["hide_when_empty"])
                        else ShopifyInventoryPolicy.CONTINUE
                    )
                    price = (
                        product_row["discounted_price"] if product_row["discounted_price"] > 0 else product_row["price"]
                    )
                    compare_at_price = product_row["price"] if product_row["discounted_price"] > 0 else None

                    variant_dto = dto.shopify.ProductVariant(
                        id=variant.id,
                        product_id=product.id,
                        sku=variant.sku,
                        price=price,
                        compare_at_price=compare_at_price,
                        inventory_policy=inventory_policy,
                    )
                    update_variant(variant_update_dto=variant_dto, shopify_variant=variant)

                    inventory_level_update = dto.shopify.InventoryLevel(
                        inventory_item_id=variant.inventory_item_id,
                        location_id=location.id,
                        available=int(np.nan_to_num(product_row["available"], nan=0)),
                    )

                    update_inventory(inventory_level_dto=inventory_level_update)
                else:
                    logger.warning(f"Not matched with POS: {product.title} - sku: {variant.sku}")
            sleep(0.5)

    logger.info("Importing products")
    for _, product_row in df.iterrows():
        if product_row.sku not in skus:
            if product_row["available"] < 1 and product_row["hide_when_empty"]:
                continue

            new_product = dto.shopify.Product(
                title=product_row["title"],
                body_html=" ".join(["<p>" + x.strip() + "</p>\n" for x in product_row["body_html"].split("\n")]),
                product_type=product_row["product_category"],
                status=settings.new_product_status,
                tags=product_row["tags"].strip(","),
                vendor=product_row["vendor"],
            )

            product = create_product(product_dto=new_product)

            price = product_row["discounted_price"] if product_row["discounted_price"] > 0 else product_row["price"]
            compare_at_price = product_row["price"] if product_row["discounted_price"] > 0 else None
            inventory_policy = (
                ShopifyInventoryPolicy.DENY if bool(product_row["hide_when_empty"]) else ShopifyInventoryPolicy.CONTINUE
            )
            new_variant = dto.shopify.ProductVariant(
                id=product.variants[0].id,
                product_id=product.id,
                sku=product_row["sku"],
                price=price,
                compare_at_price=compare_at_price,
                inventory_policy=inventory_policy,
                inventory_management=ShopifyInventoryManagement.SHOPIFY,
                fulfillment_service=ShopifyFulfillmentService.MANUAL,
                position=1,
            )
            variant = create_variant(variant_dto=new_variant)

            inventory_level_update = dto.shopify.InventoryLevel(
                inventory_item_id=variant.inventory_item_id,
                location_id=location.id,
                available=int(np.nan_to_num(product_row["available"], nan=0)),
            )

            images = add_images_to_product(
                product=product, image_list=[Image.open(io.BytesIO(product_row.images))] if product_row.images else []
            )

            if settings.add_metadata:
                metafields_data = _get_metafield_data(row=product_row)
                metafields = generate_product_metafields(data=metafields_data, product_id=product.id)
                add_metafields(metafields_dto=metafields, product=product)

            update_inventory(inventory_level_dto=inventory_level_update)
            sleep(0.5)

    logger.info("Done!")
