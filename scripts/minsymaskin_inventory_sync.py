import io
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import sleep

import numpy as np
import pandas as pd
import shopify
from dotenv import load_dotenv
from PIL import Image

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
    generate_product_metafield,
    get_all_shopify_resources,
    update_product,
    update_variant,
)

logging.getLogger("pyactiveresource").setLevel("WARNING")
logging.getLogger("PIL").setLevel("WARNING")
logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    load_dotenv()
    key = os.getenv("MINSYMASKIN_SHOPIFY_KEY")
    pwd = os.getenv("MINSYMASKIN_SHOPIFY_PWD")
    name = os.getenv("MINSYMASKIN_SHOPIFY_NAME")

    df = pd.read_pickle(Path(myshopify.__file__).parent.parent / "data" / "shopify_products_export.pickle")

    df = df.loc[
        df["product_type"].map(lambda x: x in ["Symaskiner", "Tilbehør", "Symaskintilbehør", "Bekledningsstoff"])
    ]

    df = df.loc[df["product_subtype"].map(lambda x: x not in ["Maler", "Gaver, esker og bokser"])]

    shop_url = f"https://{key}:{pwd}@{name}.myshopify.com/admin"
    shopify.ShopifyResource.set_site(value=shop_url)  # noqa

    # shop = shopify.Shop.current
    products = get_all_shopify_resources(shopify.Product)
    location = shopify.Location.find_first()

    skus = []
    logger.info("Updating products")
    for i, product in enumerate(products):
        if product.variants[0].sku in df["sku"].values:
            product_row = df.loc[df["sku"] == product.variants[0].sku].iloc[0]

            product_dto = dto.shopify.Product(
                id=product.id,
                product_type=product_row["product_type"],
                vendor=product_row["vendor"],
            )
            update_product(product_update_dto=product_dto, shopify_product=product)
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

                    # update_inventory(inventory_level_dto=inventory_level_update)
                else:
                    logger.warning(f"Not matched with POS: {product.title} - sku: {variant.sku}")
            sleep(0.25)

    logger.info("Importing products")
    for _, product_row in df.iterrows():
        if product_row.sku not in skus:
            if product_row["available"] < 1 and product_row["hide_when_empty"]:
                continue

            new_product_status = ShopifyProductStatus.DRAFT

            new_product = dto.shopify.Product(
                title=product_row["title"],
                body_html=" ".join(["<p>" + x.strip() + "</p>\n" for x in product_row["body_html"].split("\n")]),
                product_type=product_row["product_type"],
                status=new_product_status,
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

            data = {
                "price_unit": product_row["price_unit"],
                "minimum_order_quantity": 3 if product_row["price_unit"] == "desimeter" else 0,
            }
            metafields = generate_product_metafield(data=data, product_id=product.id)

            add_metafields(metafields_dto=metafields, resource=product)

            # update_inventory(inventory_level_dto=inventory_level_update)
            sleep(0.25)

    logger.info("Done!")
