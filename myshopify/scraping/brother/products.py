from collections import OrderedDict
from typing import List

from bs4 import BeautifulSoup
import json
import re
import myshopify.dto.product
from myshopify import dto
from myshopify.scraping.utils import get_image_from_url, get_page_html_from_url, get_clean_text_from_soup


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


def get_images_from_product_page(url: str) -> List[myshopify.dto.product.ProductImage]:
    product_page = get_page_html_from_url(url=url)
    soup = BeautifulSoup(product_page, "html.parser")

    return [
        myshopify.dto.product.ProductImage(
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


def get_product_from_product_page(url: str) -> dto.ProductDescription:
    """
    Parsing a Brother product page and creating a product description
    """

    product_page = get_page_html_from_url(url=url)
    soup = BeautifulSoup(product_page, "html.parser")
    product_detail_soup = soup.select_one(".product-detail--content")

    data_layer = json.loads(soup.find("script", text=re.compile("var\s+dataLayer")).text.split("= ")[1].split(";")[0])[0]
    # product_details = data_layer["detailProducts"][0]

    name = soup.select_one("title").text
    short_name = data_layer["detailProducts"][0]["name"]
    sku = data_layer["detailProducts"][0]["sku"]
    header = soup.select_one(".product-detail--container-title").find("h1", itemprop="name").text
    summary = soup.select_one(".product-detail--container-title").find("p", itemprop="description").text

    key_features = product_detail_soup.find("article", id="1")
    standard_accessory = product_detail_soup.find("article", id="2")
    detailed_description = product_detail_soup.find("article", id="overview")

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

    product_metadata = dto.ProductMetadata(
        name=name,
        short_code=short_name,
        brand="Brother",
        sku=sku,
        url=url
    )

    return dto.ProductDescription(
        name=name,
        metadata=product_metadata,
        images=get_images_from_product_page(url=url),
        header=header,
        summary=summary,
        features=get_clean_text_from_soup(key_features),
        standard_accessory=get_clean_text_from_soup(standard_accessory),
        detailed_description=get_clean_text_from_soup(detailed_description),
        optional_accessory=optional_accessory_list,
        technical_specification_dict=technical_specification_dict,
    )
