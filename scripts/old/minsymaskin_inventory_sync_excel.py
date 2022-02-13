import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd
import shopify
from dotenv import load_dotenv

import myshopify
from myshopify import dto
from myshopify.shopify.inventory import (
    create_product,
    create_variant,
    get_all_shopify_resources,
    get_number_from_string,
    update_inventory,
    update_variant,
)

logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # env_path = Path('.env')
    # load_dotenv(dotenv_path=env_path)
    load_dotenv()
    key = os.getenv("MINSYMASKIN_SHOPIFY_KEY")
    pwd = os.getenv("MINSYMASKIN_SHOPIFY_PWD")
    name = os.getenv("MINSYMASKIN_SHOPIFY_NAME")

    input_file = Path(myshopify.__file__).parent.parent / "data" / "inventory.xlsx"

    shop_url = f"https://{key}:{pwd}@{name}.myshopify.com/admin"
    shopify.ShopifyResource.set_site(value=shop_url)  # noqa

    df = pd.read_excel(io=input_file, engine="openpyxl")
    df.columns = [x.lower() for x in df.columns]

    # Some basic validations to assert that we have the correct sheet.
    # The columns varying depending on where the dump is done :-\
    assert len(df.columns) == 15, "Expected 14 columns in Excel sheet."
    assert df.columns[2] == "id", 'Expected input data to have "id" in third column'

    df.dropna(subset=["id"], axis=0, inplace=True)

    df.columns = [
        "sku",
        "title",
        "pos_id",
        "active",
        "recommended_product",
        "inventory_quantity",
        "product_type",
        "product_subtype1",
        "product_subtype2",
        "price",
        "price_discounted",
        "discount_start",
        "discount_end",
        "hide_when_empty",
        "lead_time",
    ]

    df.loc[:, "sku"] = df.loc[:, "sku"].map(lambda x: str(x))
    df.loc[:, "title"] = df.loc[:, "title"].astype(str).map(lambda x: x.replace("/xa0", ""))
    df.loc[:, "active"] = df.loc[:, "active"].astype(bool)
    df.loc[:, "inventory_quantity"] = df.loc[:, "inventory_quantity"].map(lambda x: int(get_number_from_string(x)))
    df.loc[:, "product_type"] = df.loc[:, "product_type"].astype(str)
    df.loc[:, "price"] = df["price"].map(lambda x: float(get_number_from_string(x)))
    df.loc[:, "hide_when_empty"] = df.loc[:, "hide_when_empty"].astype(bool)

    # Filter by product type and active
    df = df.loc[df["product_type"].map(lambda x: x in ["Symaskiner", "Symaskintilbehør"]), :]
    df = df.loc[df["active"].map(lambda x: x is True)]
    df = df.loc[df.apply(lambda x: x["active"] or x["title"].lower().startswith("brother"), axis=1)]

    # Trying to figure out the vendor based on name for certain items.
    df.loc[:, "vendor"] = None
    df.loc[df.loc[:, "title"].map(lambda x: "janome" in str(x).replace(" ", "").lower()), "vendor"] = "Janome"
    df.loc[df.loc[:, "title"].map(lambda x: "babylock" in str(x).replace(" ", "").lower()), "vendor"] = "Baby Lock"
    df.loc[df.loc[:, "title"].map(lambda x: "brother" in str(x).replace(" ", "").lower()), "vendor"] = "Brother"

    # shop = shopify.Shop.current
    products = get_all_shopify_resources(shopify.Product)
    location = shopify.Location.find_first()

    skus = []
    # Updating existing products (variants)
    for product in products:
        for variant in product.variants:
            skus.append(variant.sku)
            if variant.sku in df["sku"].values:
                product_row = df.loc[df["sku"] == variant.sku].iloc[0]

                logger.info(f"Updating: {variant.title} - sku: {variant.sku}")
                # We are only updating a few fields since we want description text, images, etc.

                variant_update = dto.shopify.ProductVariant(
                    id=variant.id,
                    product_id=product.id,
                    sku=variant.sku,
                    price=product_row["price"],
                    inventory_policy=dto.types.ShopifyInventoryPolicy.DENY
                    if product_row["hide_when_empty"]
                    else dto.types.ShopifyInventoryPolicy.CONTINUE,
                    inventory_management=dto.types.ShopifyInventoryManagement.SHOPIFY,
                    fulfillment_service=dto.types.ShopifyFulfillmentService.MANUAL,
                )

                update_variant(variant_update_dto=variant_update)

                inventory_level_update = dto.shopify.InventoryLevel(
                    inventory_item_id=variant.inventory_item_id,
                    location_id=location.id,
                    available=int(product_row["inventory_quantity"]),
                )
                update_inventory(inventory_level_dto=inventory_level_update)
            else:
                logger.warning(f"Not matched with POS: {product.title} - sku: {variant.sku}")

    for _, product_row in df.iterrows():
        if product_row.sku not in skus:
            logger.info(f"Importing from POS: {product_row.title} - sku: {product_row.sku}")

            new_product = dto.shopify.Product(
                title=product_row["title"],
                body_html=None,
                images=[],
                options=None,
                product_type=product_row["product_type"],
                status=dto.types.ShopifyProductStatus.ACTIVE,
                tags=",".join(product_row[["product_type", "product_subtype1", "product_subtype2"]].dropna().as_list()),
                vendor=product_row["vendor"],
                variants=None,
            )
            product = create_product(product_dto=new_product)

            new_variant = dto.shopify.ProductVariant(
                product_id=product.id,
                sku=product_row["sku"],
                price=product_row["price"],
                inventory_policy=dto.types.ShopifyInventoryPolicy.DENY
                if product_row["hide_when_empty"]
                else dto.types.ShopifyInventoryPolicy.CONTINUE,
                inventory_management=dto.types.ShopifyInventoryManagement.SHOPIFY,
                fulfillment_service=dto.types.ShopifyFulfillmentService.MANUAL,
                position=1,
            )
            variant = create_variant(variant_dto=new_variant)

            inventory_level_update = dto.shopify.InventoryLevel(
                inventory_item_id=variant.inventory_item_id,
                location_id=location.id,
                available=int(product_row["inventory_quantity"]),
            )
            update_inventory(inventory_level_dto=inventory_level_update)

    logger.info("Complete")
