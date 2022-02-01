import logging
from collections import OrderedDict
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest

from minsymaskin import dto
from minsymaskin.scraping.utils import get_image_from_url

logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("selenium").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super().formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super().format(record)
        if record.exc_text:
            s = s.replace("\n", "") + "|"
        return s


logging_format = OneLineExceptionFormatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | [%(pathname)s:%(lineno)d] | %(message)s"
)

file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()

file_handler.setFormatter(logging_format)
stream_handler.setFormatter(logging_format)

logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler])


@pytest.fixture
def product_metadata():
    dto.ProductMetadata(
        name="Sewing machine", short_code="machine1", brand="Some brand", sku="100040", url="http://www.example.com"
    )


@pytest.fixture
def some_image():
    url = "https://www.brother.eu/-/media/product-images/supplies/sewing-and-craft/sewing-machines/a80/a80_right.png"
    return dto.Image(name="a80_right", alt="Alternative text", suffix="png", url=url, image=get_image_from_url(url=url))


@pytest.fixture
def some_product(product_metadata, some_image) -> dto.Product:
    return dto.Product(
        name="Sewing machine",
        metadata=product_metadata,
        images=[some_image],
        header="Strong and sturdy!",
        summary="This is the product for you if you want quality!.",
        features_header="Features",
        features=["Feature 1", "Feature 2", "Feature 3"],
        standard_accessory_header="Standard accessory",
        standard_accessory=["Accessory 1", "Accessory 2", "Accessory 3"],
        detailed_description_header="Get to know the details!",
        detailed_description="This is an awesome product!",
        optional_accessory_header="Optional accessory",
        optional_accessory=["Option A", "Option B", "Option C"],
        technical_specification_header="Specifications",
        technical_specification_dict=OrderedDict({("weight", "9.8kg"), ("size", "120x140cm")}),
    )


@pytest.fixture
def some_shopify_product():
    return dto.ShopifyProduct(
        title="Some product name",
        sku="1000",
        inventory_quality=10,
        product_type="type1",
        price=13.30,
        hide_when_empty=True,
        vendor="Vendor1",
    )
