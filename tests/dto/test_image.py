from minsymaskin import dto
from minsymaskin.scraping.utils import get_image_from_url


def test_image_list_item():
    url = "https://www.brother.eu/-/media/product-images/supplies/sewing-and-craft/sewing-machines/a80/a80_right.png"
    image_list_item = dto.ImageListItem(
        file_name="a80_right.png", alternative_text="Alternative text", url=url, image=get_image_from_url(url=url)
    )

    assert image_list_item


def test_image_list():
    url = "https://www.brother.eu/-/media/product-images/supplies/sewing-and-craft/sewing-machines/a80/a80_right.png"
    image_list_item = dto.ImageListItem(
        file_name="a80_right.png", alternative_text="Alternative text", url=url, image=get_image_from_url(url=url)
    )

    dto.ImageList(images=[image_list_item] * 3)
