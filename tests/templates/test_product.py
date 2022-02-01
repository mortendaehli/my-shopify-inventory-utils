from myshopify.templates.product import render_product_page


def test_render_product_page(some_product):
    """
    Todo: Test all attributes. For now we keep to only testing the pure strings.
    :param some_product:
    :return:
    """
    product_page = render_product_page(product=some_product)

    for k, v in some_product.dict().items():
        if isinstance(v, str):
            assert v in product_page
