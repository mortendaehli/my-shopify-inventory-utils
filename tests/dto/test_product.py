from collections import OrderedDict

from minsymaskin import dto


def test_basic_product():
    product = dto.Product(
        name="Sewing machine",
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
        technical_specification_dict=OrderedDict({"weight": "9.8kg", "size": "120x140cm"}),
    )

    assert product


def test_product_list_item():
    product_list_item = dto.ProductListItem(product_code="product1", title="Title1", url="http://www.example.com")

    assert product_list_item


def test_product_list():
    some_product_list_item = dto.ProductListItem(product_code="product1", title="Title1", url="http://www.example.com")
    product_list = dto.ProductList(products=[some_product_list_item] * 3)

    assert product_list
