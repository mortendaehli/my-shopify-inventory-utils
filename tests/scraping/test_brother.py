from pathlib import Path

import minsymaskin
from minsymaskin import dto
from minsymaskin.scraping.brother.products import get_all_products_metadata, get_product_from_product_page

DATA_FOLDER = Path(minsymaskin.__file__).parent.parent / "data" / "tmp"
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
        url="https://sewingcraft.brother.eu/de-de/produkte/maschinen/naehmaschinen/naehmaschinen-fuer-anfaenger/innov-is-a80",
    )

    result = get_product_from_product_page(product_metadata=product_metadata)
    assert result
