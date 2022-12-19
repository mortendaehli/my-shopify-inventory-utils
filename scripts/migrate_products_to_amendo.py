import logging
import ssl
from functools import lru_cache
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import sleep
from typing import List, Optional, Union

import pandas as pd
import shopify
from pydantic import BaseSettings

from myshopify import dto
from myshopify.api.amendo import AmendoAPIClient
from myshopify.api.shopify.inventory import get_all_shopify_resources
from myshopify.config import config
from myshopify.dto.amendo import ProductDepartment

ssl._create_default_https_context = ssl._create_unverified_context  # noqa

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
    query_batch: int = 50


class AmendoProductMigrator:
    def __init__(self, settings: Settings):
        self.settings = settings
        shop_url = (
            f"https://{self.settings.shopify_key}:{self.settings.shopify_password}"
            f"@{self.settings.shopify_shop_name}.myshopify.com/admin"
        )

        self.shopify = shopify
        self.shopify.ShopifyResource.set_site(value=shop_url)  # noqa
        self.shopify_location = shopify.Location.find(67545989354)
        self.shopify_products = get_all_shopify_resources(shopify.Product)
        # self.shopify_variants = get_all_shopify_resources(shopify.Variant)
        self.amendo = AmendoAPIClient()
        self.amendo_department: Optional[List[dto.amendo.Department]] = None  # self.get_amendo_departments()
        self.amendo_product_categories: Optional[
            List[dto.amendo.Category]
        ] = None  # self.get_amendo_product_categories()
        self.amendo_product_brands: Optional[List[dto.amendo.Brand]] = None  # self.get_amendo_product_brands()
        self.amendo_product_suppliers: Optional[List[dto.amendo.Supplier]] = None  # self.get_amendo_product_suppliers()

    def get_amendo_departments(self) -> dto.amendo.Department:
        r = self.amendo.department_list_all(path_params=dto.amendo.OffsetLimitFromDatePathParams())
        if r.totalCount > 1:
            raise ValueError("We expect only 1 department")
        return r.departments[0]

    def get_amendo_products(self) -> List[dto.amendo.Product]:
        r = self.amendo.product_list_all(dto.amendo.ProductFilter(limit=self.settings.query_batch, offset=0))
        products = r.data
        for i in range(1, r.totalCount // 50):
            r = self.amendo.product_list_all(
                path_params=dto.amendo.ProductFilter(
                    limit=self.settings.query_batch, offset=self.settings.query_batch * i
                )
            )
            products.extend(r.data)
            raise ValueError("Need to QA this!")

        return products

    def get_amendo_product_categories(self) -> List[dto.amendo.Category]:
        r = self.amendo.category_list_all(
            path_params=dto.amendo.OffsetLimitFromDateSortOrderPathParams(limit=self.settings.query_batch, offset=0)
        )
        categories = r.categories
        for i in range(1, r.total_count // 50):
            r = self.amendo.category_list_all(
                path_params=dto.amendo.OffsetLimitFromDateSortOrderPathParams(
                    limit=self.settings.query_batch, offset=self.settings.query_batch * i
                )
            )
            categories.extend(r.categories)
            raise ValueError("Need to QA this!")

        return categories

    def get_amendo_product_brands(self) -> List[dto.amendo.Brand]:
        r = self.amendo.brand_list_all(
            path_params=dto.amendo.OffsetLimitFromDatePathParams(limit=self.settings.query_batch, offset=0)
        )
        brands = r.brands
        for i in range(1, r.totalCount // 50):
            r = self.amendo.brand_list_all(
                path_params=dto.amendo.OffsetLimitFromDatePathParams(
                    limit=self.settings.query_batch, offset=self.settings.query_batch * i
                )
            )
            brands.extend(r.brands)
            raise ValueError("Need to QA this!")

        return brands

    def get_amendo_product_suppliers(self) -> List[dto.amendo.Supplier]:
        r = self.amendo.supplier_list_all(
            path_params=dto.amendo.OffsetLimitFromDateSortOrderPathParams(limit=self.settings.query_batch, offset=0)
        )
        suppliers = r.suppliers
        for i in range(1, r.total_count // 50):
            r = self.amendo.supplier_list_all(
                path_params=dto.amendo.OffsetLimitFromDateSortOrderPathParams(
                    limit=self.settings.query_batch, offset=self.settings.query_batch * i
                )
            )
            suppliers.extend(r.suppliers)
            raise ValueError("Need to QA this!")

        return suppliers

    @lru_cache
    def get_or_create_category_by_name(self, category_name) -> dto.amendo.Category:
        for category in self.amendo_product_categories:
            if category.categoryName == category_name:
                return category
        category_data = self.amendo.category_create_or_update(
            body=dto.amendo.CategoryCreateBody(data=[dto.amendo.Category(categoryName=category_name)])
        )
        self.amendo_product_categories = self.get_amendo_product_categories()
        return category_data.data[0].categoryData

    @lru_cache
    def get_or_create_brand_by_name(self, brand_name) -> dto.amendo.Brand:
        for brand in self.amendo_product_brands:
            if brand.brandName == brand_name:
                return brand
        brand_data = self.amendo.brand_create_or_update(
            body=dto.amendo.BrandCreateBody(data=[dto.amendo.Brand(brandName=brand_name)])
        )
        self.amendo_product_brands = self.get_amendo_product_brands()
        return brand_data.data[0].brandData

    @lru_cache
    def get_or_create_supplier_by_name(self, supplier_name):
        for supplier in self.amendo_product_suppliers:
            if supplier.supplierName == supplier_name:
                return supplier
        supplier_data = self.amendo.supplier_create_or_update(
            body=dto.amendo.SupplierCreateOrUpdateBody(data=[dto.amendo.Supplier(supplierName=supplier_name)])
        )
        self.amendo_product_suppliers = self.get_amendo_product_suppliers()
        return supplier_data.data[0].supplierData

    def get_metafield_by_name(
        self, metafields: List[shopify.Metafield], field_name: str
    ) -> Optional[Union[float, int, str]]:
        for metafield in metafields:
            if metafield.attributes.get("key") == field_name:
                return metafield.attributes.get("value")
        return None

    def get_products(self):
        csv_columns = [
            "varenummer",
            "navn",
            "strekkode",
            "beskrivelse",
            "enhet",
            "underkategori",
            "hovedkategori",
            "produsent",
            "leverandør",
            "mvasats",
            "takeawaymvasats",
            "kostpris",
            "priseksmva",
            "prisinklmva",
            "ordreminpris",
            "takeawaypriseksmva",
            "takeawayprisinklmva",
            "åpen-pris",
            "lagerstyring",
            "vekt-påkrevet",
            "vekt-tara",
            "vekt-egen",
            "vekt-enhet",
            "kjønn",
            "selg-på-miinto",
            "bongskriver",
            "bilde",
            "bildeurl",
            "variant-hoved",
            "variant-1-navn",
            "variant-1-beskrivelse",
            "variant-2-navn",
            "variant-2-beskrivelse",
            "variant-3-navn",
            "variant-3-beskrivelse",
            "status",
            "følgesvare-varenummer",
            "følgesvare-antall",
            "følgesvare-låst",
            "følgesvare-endre",
            "kombo",
            "kombo-detaljer",
            "kombo-varenummer",
            "kombo-antall",
            "slett",
            "web-integration",
        ]
        df = pd.DataFrame(columns=csv_columns)
        for i, product in enumerate(self.shopify_products):
            logger.info(f"Exporting product: {i}/{len(self.shopify_products)}")
            # Product metafields
            try:
                shopify_metafields = product.metafields()
            except Exception:
                sleep(10)
                shopify_metafields = product.metafields()
            price_unit = self.get_metafield_by_name(metafields=shopify_metafields, field_name="price_unit")
            supplier = self.get_metafield_by_name(metafields=shopify_metafields, field_name="supplier")
            # amendo_price_unit_id = self.get_metafield_by_name(
            #     metafields=shopify_metafields, field_name="amendo_price_unit_id"
            # )
            cost_price = self.get_metafield_by_name(metafields=shopify_metafields, field_name="cost_price")
            vat_percent = self.get_metafield_by_name(metafields=shopify_metafields, field_name="vat_rate")

            product_category = self.get_metafield_by_name(metafields=shopify_metafields, field_name="product_category")
            color = self.get_metafield_by_name(metafields=shopify_metafields, field_name="product_color")
            if product_category is not None and product_category.lower() != "symaskiner":
                # Fixme: make sure this does not end up as None.
                product_group_1 = self.get_metafield_by_name(metafields=shopify_metafields, field_name="product_group1")
            else:
                product_group_1 = self.get_metafield_by_name(metafields=shopify_metafields, field_name="product_group2")
                if product_group_1 is None:
                    product_group_1 = self.get_metafield_by_name(
                        metafields=shopify_metafields, field_name="product_group1"
                    )

            image = product.attributes.get("image")
            if image is not None:
                image_url = image.attributes.get("src")
            else:
                image_url = None

            for variant in product.attributes.get("variants"):
                pris_eks_mva = None  # float(variant.attributes["price"]) / (1 + (float(shopify_vat_percent) / 100))
                df.loc[variant.attributes["sku"], "varenummer"] = variant.attributes["sku"]
                df.loc[variant.attributes["sku"], "navn"] = product.attributes["title"]
                df.loc[variant.attributes["sku"], "strekkode"] = variant.attributes["barcode"]
                df.loc[variant.attributes["sku"], "beskrivelse"] = product.attributes["body_html"]
                df.loc[variant.attributes["sku"], "enhet"] = price_unit
                df.loc[variant.attributes["sku"], "underkategori"] = product_group_1
                df.loc[variant.attributes["sku"], "hovedkategori"] = product_category
                df.loc[variant.attributes["sku"], "produsent"] = product.attributes["vendor"]
                df.loc[variant.attributes["sku"], "leverandør"] = supplier
                df.loc[variant.attributes["sku"], "mvasats"] = vat_percent
                df.loc[variant.attributes["sku"], "takeawaymvasats"] = None
                df.loc[variant.attributes["sku"], "kostpris"] = cost_price
                df.loc[variant.attributes["sku"], "priseksmva"] = pris_eks_mva
                df.loc[variant.attributes["sku"], "prisinklmva"] = variant.attributes["price"]
                df.loc[variant.attributes["sku"], "ordreminpris"] = None
                df.loc[variant.attributes["sku"], "takeawaypriseksmva"] = None
                df.loc[variant.attributes["sku"], "takeawayprisinklmva"] = None
                df.loc[variant.attributes["sku"], "åpen-pris"] = 0
                df.loc[variant.attributes["sku"], "lagerstyring"] = 1
                df.loc[variant.attributes["sku"], "vekt-påkrevet"] = 0
                df.loc[variant.attributes["sku"], "vekt-tara"] = None
                df.loc[variant.attributes["sku"], "vekt-egen"] = variant.attributes.get("weight")
                df.loc[variant.attributes["sku"], "vekt-enhet"] = variant.attributes.get("weight_unit")
                df.loc[variant.attributes["sku"], "kjønn"] = None
                df.loc[variant.attributes["sku"], "selg-på-miinto"] = None
                df.loc[variant.attributes["sku"], "bongskriver"] = None
                df.loc[variant.attributes["sku"], "bilde"] = None
                df.loc[variant.attributes["sku"], "bildeurl"] = image_url
                df.loc[variant.attributes["sku"], "variant-hoved"] = None
                df.loc[variant.attributes["sku"], "variant-1-navn"] = "Farge" if color else None
                df.loc[variant.attributes["sku"], "variant-1-beskrivelse"] = color
                df.loc[variant.attributes["sku"], "variant-2-navn"] = None
                df.loc[variant.attributes["sku"], "variant-2-beskrivelse"] = None
                df.loc[variant.attributes["sku"], "variant-3-navn"] = None
                df.loc[variant.attributes["sku"], "variant-3-beskrivelse"] = None
                df.loc[variant.attributes["sku"], "status"] = 1
                df.loc[variant.attributes["sku"], "følgesvare-varenummer"] = None
                df.loc[variant.attributes["sku"], "følgesvare-antall"] = None
                df.loc[variant.attributes["sku"], "følgesvare-låst"] = None
                df.loc[variant.attributes["sku"], "følgesvare-endre"] = None
                df.loc[variant.attributes["sku"], "kombo"] = None
                df.loc[variant.attributes["sku"], "kombo-detaljer"] = None
                df.loc[variant.attributes["sku"], "kombo-varenummer"] = None
                df.loc[variant.attributes["sku"], "kombo-antall"] = None
                df.loc[variant.attributes["sku"], "slett"] = 0
                df.loc[variant.attributes["sku"], "web-integration"] = 1

        return df[csv_columns]

    def synch_to_amendo(self):
        """Updating products that already exists in Amendo with proper data"""

        # product = self.amendo.product_view_details(dto.amendo.ProductIdPathParams(productId=3))
        logger.info("Starting product sync.")

        for product in self.shopify_products:
            logger.info(f"Updating product {product.attributes['id']}: {product.attributes['title']}")
            if product.attributes.get("status") == dto.types.ShopifyProductStatus.ACTIVE:
                # Product metafields
                shopify_metafields = product.metafields()
                shopify_supplier = self.get_metafield_by_name(metafields=shopify_metafields, field_name="supplier")
                shopify_brand = product.attributes["vendor"]
                shopify_category = product.attributes["product_type"]
                # shopify_price_unit = self.get_metafield_by_name(metafields=shopify_metafields, field_name="price_unit")
                amendo_price_unit_id = self.get_metafield_by_name(
                    metafields=shopify_metafields, field_name="amendo_price_unit_id"
                )
                shopify_cost_price = self.get_metafield_by_name(metafields=shopify_metafields, field_name="cost_price")
                shopify_vat_percent = self.get_metafield_by_name(metafields=shopify_metafields, field_name="vat_rate")
                if len(product.attributes["variants"]) == 1:
                    variant = product.attributes["variants"][0]
                    barcode = variant.attributes.get("barcode")
                    brand = self.get_or_create_brand_by_name(brand_name=shopify_brand)  # Vendor in Shopify
                    supplier = (
                        self.get_or_create_supplier_by_name(supplier_name=shopify_supplier)
                        if shopify_supplier
                        else None
                    )
                    category = self.get_or_create_category_by_name(category_name=shopify_category)
                    amendo_product = dto.amendo.Product(
                        # productId=4,
                        productName=product.attributes["title"],
                        # productNumber=variant.attributes["sku"],
                        barcode=barcode,
                        description=product.attributes["body_html"],
                        departmentId=self.amendo_department.departmentId,
                        brandId=brand.brandId,
                        categoryId=category.categoryId,
                        supplierId=supplier.supplierId,
                        productUnitId=amendo_price_unit_id,
                        vatRatePercent=shopify_vat_percent,
                        costPrice=shopify_cost_price,
                        priceIncVat=variant.attributes["price"],
                        stockControl=True,
                        showOnWeb=True,
                        images=None,  # Fixme: figure out what to do here... can we use images_url?
                        # isTakeaway=False,
                        # hasVariant=False,
                        isCombo=False,
                        # hasConnected=None,
                        # childProductsOnReceipt=None,
                        # isOpenPrice=None,  # ??
                        # printOnBong=None,
                        # variants=None,
                    )
                    response = self.amendo.product_create_or_update(  # noqa
                        body=dto.amendo.ProductCreateOrUpdateRequestBody(data=[amendo_product])
                    )

                    for variant in product.attributes.variants:
                        logger.info(f"Updating product variant {variant.attributes.id}: {variant.attributes.title}")
                        amendo_variant = dto.amendo.ProductVariant(  # noqa
                            parentId=variant.attributes.get("id"),
                            productName=product.attributes["title"],
                            productNumber=variant.attributes["sku"],
                            barcode=barcode,
                            showOnWeb=True,
                            attributes=None,
                            departments=[ProductDepartment(**self.amendo_department.__dict__)],
                        )
                    else:
                        raise NotImplementedError("This has not been implemented yet.")

    def synch_to_shopify(self) -> None:
        ...

    def get_product_stock(self):

        csv_columns = [
            "stock",
        ]
        df = pd.DataFrame(columns=csv_columns)
        df.index.name = "sku"

        for i, product in enumerate(self.shopify_products):
            logger.info(f"Exporting product stock: {i}/{len(self.shopify_products)}")
            for variant in product.attributes["variants"]:
                df.loc[variant.attributes["sku"], "stock"] = int(variant.attributes.get("inventory_quantity"))

        return df.reset_index()


if __name__ == "__main__":
    migrator = AmendoProductMigrator(settings=Settings())
    df_products = migrator.get_products()
    df_products.to_csv("product_export.csv", index=False)
    df_product_stock = migrator.get_product_stock()
    df_product_stock.to_csv("stock_export.csv", index=False, header=False)

    logger.info("Finished!")
