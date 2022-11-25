import logging
import ssl
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import List, Optional, Union

import shopify
from pydantic import BaseSettings

from myshopify import dto
from myshopify.api.amendo import AmendoAPIClient
from myshopify.config import config

ssl._create_default_https_context = ssl._create_unverified_context

logging.getLogger("pyactiveresource").setLevel("WARNING")
logging.getLogger("PIL").setLevel("WARNING")
logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / "minsymaskin.log", maxBytes=1000000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    shopify_key: str = config.QUILTEFRYD_SHOPIFY_KEY
    shopify_password: str = config.QUILTEFRYD_SHOPIFY_PWD
    shopify_shop_name: str = config.QUILTEFRYD_SHOPIFY_NAME


class AmendoProductMigrator:
    def __init__(self, settings: Settings):
        self.settings = settings
        shop_url = (
            f"https://{self.settings.shopify_key}:{self.settings.shopify_password}"
            f"@{self.settings.shopify_shop_name}.myshopify.com/admin"
        )

        self.shopify = shopify
        self.shopify.ShopifyResource.set_site(value=shop_url)
        self.shopify_location = shopify.Location.find(67545989354)

        self.amendo = AmendoAPIClient()
        self.amendo_department = self.get_amendo_departments()
        self.amendo_product_categories = self.get_amendo_product_categories()
        self.amendo_product_brands = self.get_amendo_product_brands()
        self.amendo_product_suppliers = self.get_amendo_product_suppliers()

    def get_amendo_departments(self) -> dto.amendo.Department:
        return self.amendo.department_list_all(path_params=dto.amendo.OffsetLimitFromDatePathParams()).departments[0]

    def get_amendo_product_categories(self) -> List[dto.amendo.Category]:
        return self.amendo.category_list_all(path_params=dto.amendo.OffsetLimitFromDateSortOrderPathParams()).categories

    def get_amendo_product_brands(self) -> List[dto.amendo.Brand]:
        return self.amendo.brand_list_all(path_params=dto.amendo.OffsetLimitFromDatePathParams()).brands

    def get_amendo_product_suppliers(self) -> List[dto.amendo.Supplier]:
        return self.amendo.supplier_list_all(path_params=dto.amendo.OffsetLimitFromDateSortOrderPathParams()).suppliers

    def get_or_create_category_by_name(self, category_name) -> dto.amendo.Category:
        for category in self.amendo_product_categories:
            if category.categoryName == category_name:
                return category
        category_data = self.amendo.category_create_or_update(
            body=dto.amendo.CategoryCreateBody(data=[dto.amendo.Category(categoryName=category_name)])
        )
        self.amendo_product_categories = self.get_amendo_product_categories()
        return category_data.data[0].categoryData

    def get_or_create_brand_by_name(self, brand_name) -> dto.amendo.Brand:
        for brand in self.amendo_product_brands:
            if brand.brandName == brand_name:
                return brand
        brand_data = self.amendo.brand_create_or_update(
            body=dto.amendo.BrandCreateBody(data=[dto.amendo.Brand(brandName=brand_name)])
        )
        self.amendo_product_brands = self.get_amendo_product_brands()
        return brand_data.data[0].brandData

    def get_or_create_supplier_by_name(self, supplier_name):
        for supplier in self.amendo_product_suppliers:
            if supplier.supplierName == supplier_name:
                return supplier
        supplier_data = self.amendo.supplier_create_or_update(
            body=dto.amendo.SupplierCreateOrUpdateBody(data=[dto.amendo.Supplier(supplierName=supplier_name)])
        )
        self.amendo_product_suppliers = self.get_amendo_product_suppliers()
        return supplier_data.data[0].supplierData

    def get_metafield_by_name(self, product: shopify.Product, field_name: str) -> Optional[Union[float, int, str]]:
        for metafield in product.metafields():
            if metafield.attributes.get("key") == field_name:
                return metafield.attributes.get("value")
        return None

    def run(self):
        # products = get_all_shopify_resources(shopify.Product)
        # variants = get_all_shopify_resources(shopify.Variant)
        for product in [shopify.Product.find(7616107315434)]:
            logger.info(f"Updating product {product.attributes['id']}: {product.attributes['title']}")
            if len(product.attributes["variants"]) == 1:
                shopify_supplier = self.get_metafield_by_name(product=product, field_name="supplier")
                shopify_brand = product.attributes["vendor"]
                shopify_category = product.attributes["product_type"]
                # shopify_price_unit = self.get_metafield_by_name(product=product, field_name="price_unit")
                # shopify_cost_price = self.get_metafield_by_name(product=product, field_name="cost_price")
                # shopify_vat_percent = self.get_metafield_by_name(product=product, field_name="vat_percent")
                variant = product.attributes["variants"][0]
                brand = self.get_or_create_brand_by_name(brand_name=shopify_brand)  # Vendor in Shopify
                supplier = (
                    self.get_or_create_supplier_by_name(supplier_name=shopify_supplier) if shopify_supplier else None
                )
                category = self.get_or_create_category_by_name(category_name=shopify_category)
                amendo_product = dto.amendo.Product(  # noqa
                    productId=product.attributes["id"],
                    productName=product.attributes["title"],
                    productNumber=variant.attributes["sku"],
                    barcode=None,  # Fixme: Get from metadata
                    description=product.attributes["body_html"],
                    departmentId=self.amendo_department.departmentId,
                    brandId=brand.brandId,
                    categoryId=category.categoryId,
                    supplierId=supplier.supplierId,
                    productUnitId=None,  # Fixme: Get from metadata
                    vatRateId=None,
                    vatRatePercent=None,  # Fixme: Get from metadata
                    costPrice=None,  # Fixme: Get from metadata
                    priceIncVat=variant.attributes["price"],
                    stockControl=True,
                    showOnWeb=True,
                    images=None,  # Fixme: figure out what to do here... can we use images_url?
                    isTakeaway=False,
                    hasVariant=False,
                    isCombo=False,
                    hasConnected=None,
                    childProductsOnReceipt=None,
                    isOpenPrice=None,  # ??
                    printOnBong=None,
                    variants=None,
                )
            else:
                for variant in product.attributes.variants:
                    logger.info(f"Updating product variant {variant.attributes.id}: {variant.attributes.title}")
                    # amendo_variant = dto.amendo.ProductVariant(
                    #     parentId=...,
                    #     productName=...,
                    #     productNumber=...,
                    #     barcode=...,
                    #     showOnWeb=...,
                    #     attributes=...,
                    #     departments=...,
                    # )
                raise NotImplementedError("This has not been implemented yet.")


if __name__ == "__main__":
    migrator = AmendoProductMigrator(settings=Settings())
    migrator.run()
    logger.info("Finished!")
