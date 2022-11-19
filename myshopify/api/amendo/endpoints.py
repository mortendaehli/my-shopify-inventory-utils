from apiclient.decorates import endpoint


@endpoint(base_url="https://api.tellix.no/web/v3/")
class Endpoints:
    # Auth
    generate_token: str = "/getaccesstoken"

    # Brand
    brand_list_all: str = "/brand/list"
    brand_create_or_update: str = "/brand/save"
    brand_view_details: str = "/brand/view"

    # Product category
    product_category_list_all: str = "/category/list"
    product_category_create_or_update: str = "/category/save"
    product_category_view_details: str = "/category/view"

    # Customer
    customer_list_all: str = "/customer/list"
    customer_create_or_update: str = "/customer/save"
    customer_update_by_id: str = "/customer/update/{id}"
    customer_view_details: str = "/customer/view"

    # Department
    department_view_info: str = "/department/info"
    department_list_all: str = "/department/list"

    # Order
    order_list_all: str = "/order/list"
    order_in_back_office_create: str = "/order/orderhandling/save"
    order_in_back_office_view_details: str = "/order/orderhandling/view"
    order_view_details_by_id: str = "/order/{id}"

    # Product Orders
    products_order_info: str = "/products-order/info"

    # Stock
    product_stock_list_all: str = "/allproducts/stock/info"
    product_stock_add_receive: str = "/product-receive/add"
    product_stock_adjust: str = "/stock/adjust"
    product_stock_view: str = "/stock/info"
    product_stock_set: str = "/stock/set"
    product_stock_update: str = "/stock/update"
    product_stock_module_status: str = "/stockmodule/status"

    # Products
    product_list_all: str = "/product/list"
    product_create_or_update: str = "/product/save"
    product_update_by_id: str = "/product/update{id}"
    product_update_updated_at: str = "/product/updateUpdatedAt"
    product_variant_create: str = "/product/variant"
    product_view_details: str = "/product/view"

    # Report
    report_list_all_z: str = "/zreport/list"

    # Sales report
    sales_report_list_all: str = "/salesreport/list"

    # Supplier
    supplier_list_all: str = "/supplier/list"
    supplier_create_or_update: str = "/supplier/save"
    supplier_view_details: str = "/supplier/view"

    # Variant group
    variant_group_list_all: str = "/variantgroup/list"
    variant_group_create_or_update: str = "/variantgroup/save"

    # VAT rate
    var_rate_list_all: str = "/vatrate/list"
    vat_rate_create_or_update: str = "/vatrate/save"
    var_rate_view_details: str = "/vatrate/view"
