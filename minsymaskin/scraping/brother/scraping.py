from bs4 import BeautifulSoup

from minsymaskin import dto
from minsymaskin.scraping.utils import get_image_from_url, get_page_html_from_url


def get_product_list_page(page_number: int = 1):
    return get_page_html_from_url(
        url=f"https://sewingcraft.brother.eu/de-de/produkte/alle-produkte?count=48&sort=name-asc&page={page_number}#Results"
    )


def get_all_products() -> dto.ProductList:
    _all_products = []
    for page_number in [1, 2]:
        product_list_page = get_product_list_page(page_number=page_number)
        soup = BeautifulSoup(product_list_page, "html.parser")
        product_soups = soup.select(".product-results > .row > div")
        for product_soup in product_soups:
            _all_products.append(
                dto.ProductListItem(
                    title="Brother " + product_soup.select_one(".product-results--item--title").text,
                    sku=None,
                    product_code=product_soup.select_one(".product-results--item--title")
                    .find("a")["href"]
                    .split("/")[-1],
                    url=product_soup.select_one(".product-results--item--title").find("a")["href"],
                )
            )

    return dto.ProductList(products=_all_products)


def get_images_from_product_page(url: str) -> dto.ImageList:
    product_page = get_page_html_from_url(url=url)
    soup = BeautifulSoup(product_page, "html.parser")

    return dto.ImageList(
        images=[
            dto.ImageListItem(
                file_name=image["src"].split(".png")[0].split("/")[-1],
                alternative_text=image["alt"],
                url=image["src"].split("?")[0],
                image=get_image_from_url(url=image["src"].split("?")[0]),
            )
            for i, image in enumerate(
                soup.select_one(".product-detail--container-gallery").select_one(".product-carousel").find_all("img")
            )
        ]
    )


def get_product_from_product_page(url: str) -> dto.Product:
    """
    Parsing a Brother product page and creating a product description
    """

    product_page = get_page_html_from_url(url=url)
    soup = BeautifulSoup(product_page, "html.parser")
    name = soup.select_one("title").text

    # <div class="col-xs-12 col-md-6 product-detail--container-title">
    header = soup.select_one(".product-detail--container-title").find("h1", itemprop="name").text
    summary = soup.select_one(".product-detail--container-title").find("p", itemprop="description").text
    sku = soup.select_one(".product-detail--container-title").find("p", itemprop="sku").text

    product_detail_soup = soup.select_one(".product-detail--content")
    detailed_description = product_detail_soup.find("article", id="overview")
    features = product_detail_soup.find("article", id="1")
    features_list = [x.text for x in features.findAll("li") if x.text]
    standard_accessory = product_detail_soup.find("article", id="2")
    standard_accessory_list = [x.text for x in standard_accessory.findAll("li") if x.text]
    optional_accessory = product_detail_soup.find("article", id="supplies")  # Todo: Clean me
    technical_specification_dict = product_detail_soup.find("article", id="specifications")  # Todo: Clean me

    return dto.Product(
        name=name,
        sku=sku,
        brand="Brother",
        header=header,
        summary=summary,
        features_header=None,  # Egenskaper
        features=features_list,
        standard_accessory_header=None,
        standard_accessory=standard_accessory_list,
        detailed_description_header=None,
        detailed_description=detailed_description,
        optional_accessory_header=None,
        optional_accessory=optional_accessory,
        technical_specification_header=None,
        technical_specification_dict=technical_specification_dict,
    )
