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
from myshopify.shopify.inventory import (
    add_images_to_product,
    create_product,
    create_variant,
    get_all_shopify_resources,
    update_inventory,
    update_variant,
    update_product,
delete_product,
delete_variant,
add_metafields
)

logging.getLogger("pyactiveresource").setLevel("WARNING")
logging.getLogger("PIL").setLevel("WARNING")
logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | [%(pathname)s:%(lineno)d] | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # env_path = Path('.env')
    # load_dotenv(dotenv_path=env_path)
    load_dotenv()
    key = os.getenv("QUILTEFRYD_SHOPIFY_KEY")
    pwd = os.getenv("QUILTEFRYD_SHOPIFY_PWD")
    name = os.getenv("QUILTEFRYD_SHOPIFY_NAME")

    df = pd.read_pickle(Path(myshopify.__file__).parent.parent / "data" / "shopify_products_export.pickle")

    shop_url = f"https://{key}:{pwd}@{name}.myshopify.com/admin"
    shopify.ShopifyResource.set_site(value=shop_url)  # noqa

    delete_all = True
    if delete_all:
        products = get_all_shopify_resources(shopify.Product)
        variants = get_all_shopify_resources(shopify.Variant)
        for variant in variants:
            logger.info(f"Deleting variant: {variant.title} - sku: {variant.sku}")
            delete_variant(variant=variant)
            sleep(0.25)
        for product in products:
            logger.info(f"Deleting product: {product.title}")
            delete_product(product=product)
            sleep(0.25)

    # shop = shopify.Shop.current
    products = get_all_shopify_resources(shopify.Product)
    location = shopify.Location.find_first()

    skus = []
    # Updating existing products (variants)
    for i, product in enumerate(products):
        if product.variants[0].sku in df["sku"].values:
            logger.info(f"Updating Product: {product.title} - sku: {product.variants[0].sku}")
            product_row = df.loc[df["sku"] == product.variants[0].sku].iloc[0]
            product_dto = dto.shopify.Product(
                title=product_row["title"],
                body_html=None,
                images=None,
                options=None,
                product_type=product_row["product_type"],
                status=dto.types.ShopifyProductStatus.ACTIVE.value,
                tags=product_row["tags"].strip(","),
                vendor=product_row["vendor"],
                variants=None,
            )
            update_product(product_update_dto=product_dto)
            for variant in product.variants:
                skus.append(variant.sku)
                if variant.sku in df["sku"].values:

                    logger.info(f"Updating Variant: {variant.title} - sku: {variant.sku}")
                    # We are only updating a few fields since we want description text, images, etc.

                    variant_dto = dto.shopify.ProductVariant(
                        id=variant.id,
                        product_id=product.id,
                        sku=variant.sku,
                        price=product_row["price"],
                        inventory_policy=dto.types.ShopifyInventoryPolicy.DENY.value
                        if bool(product_row["hide_when_empty"])
                        else dto.types.ShopifyInventoryPolicy.CONTINUE.value,
                        inventory_management=dto.types.ShopifyInventoryManagement.SHOPIFY.value,
                        fulfillment_service=dto.types.ShopifyFulfillmentService.MANUAL.value,
                    )
                    update_variant(variant_update_dto=variant_dto)

                    inventory_level_update = dto.shopify.InventoryLevel(
                        inventory_item_id=variant.inventory_item_id,
                        location_id=location.id,
                        available=int(np.nan_to_num(product_row["available"], nan=0)),
                    )

                    update_inventory(inventory_level_dto=inventory_level_update)
                else:
                    logger.warning(f"Not matched with POS: {product.title} - sku: {variant.sku}")
            sleep(0.25)

    for _, product_row in df.iterrows():
        if product_row.sku not in skus:
            logger.info(f"Importing from POS: {product_row.title} - sku: {product_row.sku}")

            new_product = dto.shopify.Product(
                title=product_row["title"],
                body_html=" ".join(["<p>" + x.strip() + "</p>\n" for x in product_row["body_html"].split("\n")]),
                images=None,
                options=None,
                product_type=product_row["product_type"],
                status=dto.types.ShopifyProductStatus.ACTIVE.value,
                tags=product_row["tags"].strip(","),
                vendor=product_row["vendor"],
                variants=None,
            )

            product = create_product(product_dto=new_product)

            new_variant = dto.shopify.ProductVariant(
                id=product.variants[0].id,
                product_id=product.id,
                sku=product_row["sku"],
                price=product_row["discounted_price"] if product_row["discounted_price"] > 0 else product_row["price"],
                compare_at_price=product_row["price"],
                inventory_policy=dto.types.ShopifyInventoryPolicy.DENY.value
                if bool(product_row["hide_when_empty"])
                else dto.types.ShopifyInventoryPolicy.CONTINUE.value,
                inventory_management=dto.types.ShopifyInventoryManagement.SHOPIFY.value,
                fulfillment_service=dto.types.ShopifyFulfillmentService.MANUAL.value,
                position=1,
            )
            variant = create_variant(variant_dto=new_variant)

            inventory_level_update = dto.shopify.InventoryLevel(
                inventory_item_id=variant.inventory_item_id,
                location_id=location.id,
                available=int(np.nan_to_num(product_row["available"], nan=0)),
            )

            images = add_images_to_product(product=product, image_list=[Image.open(io.BytesIO(product_row.images))] if product_row.images else [])
            metafields = list()
            if product_row["price_unit"]:

                metafields.append(dto.shopify.Metafield(
                    owner_id=product.id,
                    owner_resource="product",
                    key="price_unit",
                    namespace="inventory",
                    value=product_row["price_unit"],
                    type=dto.types.ShopifyType.single_line_text_field,
                    value_type=dto.types.ShopifyValueType.string
                ))

            metafields.append(dto.shopify.Metafield(
                owner_id=product.id,
                owner_resource="product",
                key="minimum_order_quantity",
                namespace="inventory",
                value=3 if product_row["price_unit"] == "desimeter" else 0,
                type=dto.types.ShopifyType.number_integer,
                value_type=dto.types.ShopifyValueType.integer
            )
            )

            add_metafields(metafields_dto=metafields, resource=product)

            update_inventory(inventory_level_dto=inventory_level_update)
            sleep(0.25)
