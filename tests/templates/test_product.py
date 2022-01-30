from minsymaskin.templates.product import render_product_page


def test_render_product_page(some_product):

    product_page = render_product_page(product=some_product)

    for k, v in some_product.dict().items():
        if isinstance(v, str):
            assert v in product_page
        elif isinstance(v, dict):
            for value in v.values():
                assert value in product_page
        elif isinstance(v, list):
            for item in v:
                assert item in product_page
        else:
            raise ValueError(f"Value {v} not found in the product_page.")
