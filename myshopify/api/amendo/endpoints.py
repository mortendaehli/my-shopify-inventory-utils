from apiclient.decorates import endpoint


@endpoint(base_url="https://api.tellix.no/web/v3/")
class Endpoints:
    list_all_brands: str = "/brand/list?offset={offset}&limit={limit}&from_date={from_date}"
    create_or_update_brand: str = "/brand/save"
    view_brands_details: str = "/brand/view?brandId={brand_id}"

    list_all_product_categories: str = (
        "/category/list?offset={offset}&limit={limit}&from_date={from_date}&sort_order={sort_order}"
    )
    create_or_update_category: str = "/category/save"
    view_product_category_details: str = "/category/view?categoryId={category_id}"
    list_all_customers: str = "/customer/list?offset={offset}&limit={limit}"
    update_customer: str = "/customer/save"
    view_customers_detail: str = "/customer/view?customerId={customer_id}"
    view_department: str = "/department/info/departmentId={department_id}"
    list_all_departments: str = "/department/list?offset={offset}&limit={limit}&from_date={from_date}"
    generate_token: str = "/getaccesstoken"
    list_all_orders: str = "/order/list?offset={offset}&limit={limit}&from_date={from_date}"
    create_new_order_in_backoffice: str = "/order/orderhandling/save"
    view_an_order_details: str = "/order/orderhandling/view?orderNumber={order_number}"
    view_an_orders_detail: str = "/order/{id}"
    list_all_product: str = "/product/list?offset={offset}&limit={limit}&filter[lastUpdateDate]={filter_last_update_date}&filter[productId]={filter_product_id}&filter[productName]={filter_product_name}&filter[productNumber]={filter_product_number}&filter[barcode]={filter_barcode}&from_date={from_date}&catgeoryId={catgeory_id}&filter[isActive]={filter_is_active}&filter[isDeleted]={filter_is_deleted}&filter[isTakeaway]={filter_is_takeaway}&order_by={order_by}&sort_by={sort_by}"
    update_product: str = "/product/save"
    view_products_detail: str = "/product/view?productId={product_id}"
    adjust_product_stock: str = "/stock/adjust"
    fetch_products_stock: str = "/stock/info?product_id={product_id}&department_id={department_id}"
    set_product_stock: str = "/stock/set"
    list_all_suppliers: str = "/supplier/list?offset={offset}&limit={limit}&from_date={from_date}"
    update_supplier: str = "/supplier/save"
    view_suppliers_details: str = "/supplier/view?supplierId={supplier_id}"
    list_all_vat_rates: str = "/vatrate/list?offset={offset}&limit={limit}&from_date={from_date}"
    create_new_vat_rate: str = "/vatrate/save"
    update_vat_rate: str = "/vatrate/save"
    view_vat_rates_details: str = "/vatrate/view?vatRateId={vat_rate_id}"
    list_all_z_reports: str = "/zreport/list?offset={offset}&limit={limit}"
