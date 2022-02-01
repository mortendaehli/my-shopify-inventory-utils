from collections import OrderedDict
from typing import List

from bs4 import BeautifulSoup

from minsymaskin import dto
from minsymaskin.scraping.utils import get_image_from_url, get_page_html_from_url


def get_product_list_page(page_number: int = 1):
    return get_page_html_from_url(
        url=f"https://sewingcraft.brother.eu/de-de/produkte/alle-produkte?count=48&sort=name-asc&page={page_number}#Results"
    )


def get_all_products_metadata() -> List[dto.ProductMetadata]:
    product_list = []
    for page_number in [1, 2]:
        product_list_page = get_product_list_page(page_number=page_number)
        soup = BeautifulSoup(product_list_page, "html.parser")
        product_soups = soup.select(".product-results > .row > div")
        for product_soup in product_soups:
            product_list.append(
                dto.ProductMetadata(
                    name="Brother " + product_soup.select_one(".product-results--item--title").text,
                    short_code=product_soup.select_one(".product-results--item--title")
                    .find("a")["href"]
                    .split("/")[-1],
                    brand="Brother",
                    sku=None,
                    url=product_soup.select_one(".product-results--item--title").find("a")["href"],
                )
            )

    return product_list


def get_images_from_product_page(url: str) -> List[dto.Image]:
    product_page = get_page_html_from_url(url=url)
    soup = BeautifulSoup(product_page, "html.parser")

    return [
        dto.Image(
            name=image["src"].split(".png")[0].split("/")[-1],
            alt=image["alt"],
            suffix=".png",
            url=image["src"].split("?")[0],
            image=get_image_from_url(url=image["src"].split("?")[0]),
        )
        for i, image in enumerate(
            soup.select_one(".product-detail--container-gallery").select_one(".product-carousel").find_all("img")
        )
    ]


def get_product_from_product_page(product_metadata: dto.ProductMetadata) -> dto.Product:
    """
    Parsing a Brother product page and creating a product description
    """

    product_page = get_page_html_from_url(url=product_metadata.url)
    soup = BeautifulSoup(product_page, "html.parser")
    name = soup.select_one("title").text

    header = soup.select_one(".product-detail--container-title").find("h1", itemprop="name").text
    summary = soup.select_one(".product-detail--container-title").find("p", itemprop="description").text
    product_metadata.sku = soup.select_one(".product-detail--container-title").find("p", itemprop="sku").text
    product_detail_soup = soup.select_one(".product-detail--content")

    standard_accessory = product_detail_soup.find("article", id="2")
    standard_accessory_list = [x.text for x in standard_accessory.findAll("li") if x.text]

    detailed_description = "\n".join([x.text for x in product_detail_soup.find("article", id="overview").find_all("a")])

    features = product_detail_soup.find("article", id="1")
    features_list = [x.text for x in features.findAll("li") if x.text]

    optional_accessory = product_detail_soup.find("article", id="supplies")
    optional_accessory_list = [
        dto.ProductMetadata(
            name=x.select_one("h4").text.strip(),
            short_code=x.select_one("a")["href"].split("/")[-1],
            brand="Brother",
            sku=None,
            url=x.select_one("a")["href"],
        )
        for x in optional_accessory.findAll("li")
    ]
    technical_specifications = product_detail_soup.find("article", id="specifications")  # Todo: Clean me
    technical_specification_dict = OrderedDict(
        {
            k: v
            for k, v in zip(
                [x.text for x in technical_specifications.find_all("th")],
                [x.text for x in technical_specifications.find_all("td")],
            )
        }
    )

    return dto.Product(
        name=name,
        metadata=product_metadata,
        header=header,
        summary=summary,
        features_header=None,
        features=features_list,
        standard_accessory_header=None,
        standard_accessory=standard_accessory_list,
        detailed_description_header=None,
        detailed_description=detailed_description,
        optional_accessory_header=None,
        optional_accessory=optional_accessory_list,
        technical_specification_header=None,
        technical_specification_dict=technical_specification_dict,
    )
