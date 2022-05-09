from pathlib import Path

import pytest

import myshopify
from myshopify import dto
from myshopify.scraping.brother.products import get_all_products_metadata, get_product_from_product_page

DATA_FOLDER = Path(myshopify.__file__).parent.parent / "data" / "tmp"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


def test_get_all_products():
    all_products = get_all_products_metadata()
    assert all_products


def test_parse_product():
    product_metadata = dto.ProductMetadata(
        name="Innov-is A80",
        short_code="innov-is-a80",
        brand="Brother",
        sku="320",
        url="https://sewingcraft.brother.eu/de-at/produkte/maschinen/sewing-machines/beginner-sewing-machines/kd40",
    )

    result = get_product_from_product_page(url=product_metadata.url)
    assert result
