from pathlib import Path

import minsymaskin
from minsymaskin.scraping.brother.scraping import get_all_products, get_product_from_product_page

DATA_FOLDER = Path(minsymaskin.__file__).parent.parent / "data" / "tmp"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)


def test_get_all_products():
    all_products = get_all_products()
    assert all_products


def test_parse_product():

    result = get_product_from_product_page(
        url="https://sewingcraft.brother.eu/de-de/produkte/maschinen/naehmaschinen/naehmaschinen-fuer-anfaenger/innov-is-a80"
    )
    assert result
