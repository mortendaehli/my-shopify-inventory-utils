from datetime import date

import pytest

import myshopify.dto.amendo as dto
from myshopify.api.amendo.client import AmendoAPIClient


class TestAmendoAPIClient:
    def setup_class(self):
        self.api = AmendoAPIClient()

    @pytest.mark.integtest
    def test_auth(self):
        response = self.api._authentication_method
        assert "Authorization" in response.get_headers().keys()

    def test_list_all_brands(self):
        response = self.api.brand_list_all(
            path_params=dto.OffsetLimitFromDatePathParams(fromDate=date(2020, 1, 1), offset=0, limit=100)
        )
        assert isinstance(response, dto.BrandList)

    def test_create_new_brand(self):
        brand = dto.Brand(brandId=1, brandName="Test brand 1", isActive=True, isDeleted=False)
        response = self.api.brand_create_or_update(body=dto.BrandCreateBody(data=[brand]))
        assert isinstance(response, dto.BrandCreateResponse)

    def test_view_brand_details(self):
        response = self.api.brand_view_details(path_params=dto.BrandIdPathParams(brandId=1))
        assert isinstance(response, dto.BrandViewResponse)

    def test_list_all_categories(self):
        response = self.api.category_list_all(path_params=dto.OffsetLimitFromDateSortOrderPathParams())
        assert isinstance(response, dto.CategoryListResponse)

    def test_category_create_or_update(self):
        category = dto.Category(categoryId=1, categoryName="Test category 1", isActive=True, isDeleted=False)
        response = self.api.category_create_or_update(body=dto.CategoryCreateBody(data=[category]))
        assert isinstance(response, dto.CategorySaveResponse)

    def test_view_product_category_details(self):
        response = self.api.category_view_details(path_params=dto.CategoryIdPathParams(categoryId=1))
        assert isinstance(response, dto.CategoryDetailResponse)

    def test_customer_list_all(self):
        response = self.api.customer_list_all(path_params=dto.OffsetLimitFromDateSortOrderPathParams())
        assert isinstance(response, dto.CustomerList)

    def test_customer_create_or_update(self):
        response = self.api.customer_create_or_update(
            body=dto.CustomerSavePostRequest(
                data=[
                    dto.Customer(customerId=1, name="Test Customer 1", country="Norway", isActive=True, isDeleted=False)
                ]
            )
        )
        assert isinstance(response, dto.CustomerSaveResponse)

    @pytest.mark.skip(reason="Does not find the customer. Something is strange here...")
    def test_customer_update_by_id(self):
        response = self.api.customer_update_by_id(
            customer_id=1,
            body=dto.CustomerUpdatePostRequest(
                data=dto.Customer(
                    name="Test Customer 1", email="test@mail.com", country="Norway", isActive=True, isDeleted=False
                )
            ),
        )
        assert isinstance(response, dto.BaseResponse)

    def test_customer_view_details(self):
        response = self.api.customer_view_details(path_params=dto.CustomerIdPathParams(customerId=1))
        assert isinstance(response, dto.CustomerViewResponse)

    def test_department_view_info(self):
        response = self.api.department_view_info(parth_params=dto.DepartmentIdPathParams(departmentId=1))
        assert isinstance(response, dto.DepartmentViewResponse)

    def test_department_list_all(self):
        response = self.api.department_list_all(path_params=dto.OffsetLimitFromDatePathParams())
        assert isinstance(response, dto.DepartmentListResponse)

    def test_order_list_all(self):
        response = self.api.order_list_all(
            path_params=dto.OffsetLimitFromDateSortOrderPathParams(offset=0, limit=50, sortOrder=dto.SortOrder.ASC)
        )
        assert isinstance(response, dto.OrderListResponse)

    @pytest.mark.skip(reason="Order handling module\\/settings is disabled")
    def test_order_create_new_in_back_office(self):
        response = self.api.order_create_new_in_back_office(
            body=dto.OrderNewInBackOfficeBody(
                data=[
                    dto.BackOfficeOrderData(
                        orderData=dto.OrderData(departmentId=1, customerId=1, comments="Some comment", status=""),
                        productData=[
                            dto.ProductData(
                                productId=1,
                                quantity=1,
                                priceIncVat=100,
                                comments="Some comment",
                                referenceComment="Some reference",
                            )
                        ],
                    )
                ]
            )
        )
        assert isinstance(response, dto.OrderInBackOfficeNewResponse)

    @pytest.mark.skip(reason="Order handling module\\/settings is disabled")
    def test_order_in_back_office_view_details(self):
        response = self.api.order_in_back_office_view_details(path_params=dto.OrderNumberPathParams(orderNumber=1))
        assert isinstance(response, dto.OrderInBackOfficeViewDetailsResponse)

    @pytest.mark.skip(reason="No orders in the system")
    def test_order_view_details_by_id(self):
        response = self.api.order_view_details_by_id(path_params=dto.IdPathParams(id=1))
        assert isinstance(response, dto.OrderViewDetailsResponse)

    def test_products_order_info(self):
        response = self.api.products_order_info(path_params=dto.OrderStatusLimitOffsetOrderByParams())
        assert isinstance(response, dto.ProductsOrderInfoResponse)

    @pytest.mark.skip(reason="Fixme: Error when contacting endpoint")
    def test_product_stock_all_products_info(self):
        response = self.api.product_stock_all_products_info(
            body=dto.StockAllProductInfoRequestBody(
                params=dto.StockAllProductInfoParams(stockDepartment=1, fromDate=date(2020, 1, 1))
            )
        )
        assert isinstance(response, dto.StockAllProductInfoResponseBody)

    @pytest.mark.skip(reason="Fixme: 500 error")
    def test_product_stock_add(self):
        response = self.api.product_stock_add(
            body=dto.ProductStockAddRequestBody(
                data=dto.ProductStockAddData(
                    department_id=1,
                    products=[
                        dto.ProductStockAddProductData(productId=1, productCount=1),
                    ],
                )
            ),
            path_params=dto.ProductIdOrderIdPathParams(productId=1),
        )
        assert isinstance(response, dto.ProductsOrderInfoResponse)

    @pytest.mark.skip(reason="Fixme: Product not assigned to the department.")
    def test_product_stock_adjust(self):
        response = self.api.product_stock_adjust(
            body=dto.ProductStockAdjustPostRequest(
                data=dto.ProductStockAdjustPostRequestData(
                    department_id=1,
                    product_id=1,
                    adjust_stock_quantity=1,
                )
            ),
            product_id=1,
        )
        assert isinstance(response, dto.ProductStockAdjustResponse)

    @pytest.mark.skip(reason="Fixme: Arguments seems wrong...? product_id and department_id instead?")
    def test_product_stock_view(self):
        response = self.api.product_stock_view(path_params=dto.IdPathParams(id=1))
        assert isinstance(response, dto.ProductsOrderInfoResponse)

    @pytest.mark.skip(reason="400 Error: Bad Request for url: https://api.tellix.no/web/v3/stock/set?id=1")
    def test_product_stock_set(self):
        response = self.api.product_stock_set(
            body=dto.ProductStockSetPostRequest(
                data=dto.ProductStockSetPostRequestData(department_id=1, product_id=1, stock_quantity=1)
            ),
            product_id=1,
        )
        assert isinstance(response, dto.ProductStockAdjustResponse)

    @pytest.mark.skip(reason="400 Error: Bad Request for url: https://api.tellix.no/web/v3/stock/update")
    def test_product_stock_update(self):
        self.api.product_stock_update(
            body=dto.ProductStockUpdateRequestBody(
                params=dto.ProductStockUpdateData(stockQuantity=1, stockDepartment=1, productNumber=1)
            )
        )

    def test_product_stock_module_status(self):
        response = self.api.product_stock_module_status()
        assert isinstance(response, dto.BaseResponse)

    def test_product_list_all(self):
        response = self.api.product_list_all(path_params=dto.ProductFilter())
        assert isinstance(response, dto.ProductListResponse)

    def test_product_create_or_update(self):
        response = self.api.product_create_or_update(
            body=dto.ProductCreateOrUpdateRequestBody(
                data=[
                    dto.Product(
                        productId=1,
                        productName="Test Product 1",
                        productNumber="1",
                        categoryId=1,
                        supplierId=1,
                        departmentId=1,
                        brandId=1,
                        priceIncVat=1.0,
                        barcode="testproductbarcode1",
                        description="test product description",
                        costPrice=0.5,
                        vatRatePercent=10,
                        isTakeaway=False,
                        stockControl=True,
                        isActive=True,
                        isDeleted=False,
                        showOnWeb=False,
                    )
                ]
            )
        )
        assert isinstance(response, dto.ProductPostResponse)

    def test_product_update_by_id(self):
        response = self.api.product_update_by_id(
            body=dto.ProductUpdateByIdRequestBody(
                data=dto.Product(
                    productId=3,
                    productName="Test product 3",
                    productNumber="3",
                    categoryId=1,
                    priceIncVat=1.0,
                    barcode="Test Bar Code 3",
                    brandId=1,
                    description="test product description 3",
                    costPrice=1,
                    vatRatePercent=25,
                    isTakeaway=False,
                    stockControl=True,
                    isActive=True,
                    isDeleted=False,
                    showOnWeb=False,
                )
            ),
            product_id=1,
        )
        assert isinstance(response, dto.BaseResponse)

    def test_product_variant_create_or_update(self):
        """Note: Need to create variant groups before doing this... Otherwise it will fail..."""
        response = self.api.product_variant_create_or_update(
            body=dto.ProductVariantCreateOrUpdateRequestBody(
                data=[
                    dto.ProductVariant(
                        parentId=1,
                        productNumber="1",
                        barcode="testproductbarcodevariant1",
                        isActive=True,
                        isDeleted=False,
                        showOnWeb=False,
                        attributes=[
                            {"variant-group": "Colors", "variant-value": "Red"},
                            {"variant-group": "Size", "variant-value": "Small"},
                        ],
                        departments=[
                            dto.ProductDepartment(
                                departmentId=1,
                                stockQuantity=1,
                                incPrice=1.0,
                                takeawayIncPrice=1.0,
                            )
                        ],
                    )
                ]
            ),
        )
        assert isinstance(response, dto.ProductVariantPostResponse)

    def test_product_view_details(self):
        response = self.api.product_view_details(path_params=dto.ProductIdPathParams(productId=3))
        assert isinstance(response, dto.ProductViewDetailsResponse)

    def test_report_list_all_z(self):
        response = self.api.report_list_all_z(path_params=dto.OffsetLimitPathParams(limit=50))
        assert isinstance(response, dto.ZReportResponse)

    def test_report_sales(self):
        response = self.api.report_sales(path_params=dto.OffsetLimitPathParams(limit=50))
        assert isinstance(response, dto.SalesReportResponse)

    def test_supplier_list_all(self):
        response = self.api.supplier_list_all(
            path_params=dto.OffsetLimitFromDateSortOrderPathParams(fromDate=date(2020, 1, 1), offset=0, limit=50)
        )
        assert isinstance(response, dto.SupplierListAllResponse)

    def test_supplier_create_or_update(self):
        supplier = dto.Supplier(supplierId=1, supplierName="Test supplier 1")
        response = self.api.supplier_create_or_update(body=dto.SupplierCreateOrUpdateBody(data=[supplier]))
        assert isinstance(response, dto.SupplierCreateOrUpdateResponse)

    @pytest.mark.skip(reason="422 Error: No Supplier found with given id.")
    def test_supplier_view_details(self):
        response = self.api.supplier_view_details(path_params=dto.SupplierIdPathParams(supplierId=1))
        assert isinstance(response, dto.SupplierViewDetailsResponse)

    @pytest.mark.skip(reason="400 Error: Bad Request for url")
    def test_variant_group_list_all(self):
        response = self.api.variant_group_list_all(
            path_params=dto.OffsetLimitFromDateSortOrderPathParams(fromDate=date(2020, 1, 1), offset=0, limit=50)
        )
        assert isinstance(response, dto.VariantGroupListAllResponse)

    @pytest.mark.skip(reason="422 Error: Unprocessable Entity for url")
    def test_variant_group_create_or_update(self):
        variant_group = dto.VariantGroupCreateOrUpdateBody(
            data=dto.VariantGroupData(
                variantGroupId=1,
                variantGroupName="Test variant group 1",
                variantValues=[dto.VariantValue(variantValueId=1, variantValue="Test value 1")],
            )
        )
        response = self.api.variant_group_create_or_update(body=variant_group)
        assert isinstance(response, dto.VariantGroupCreateOrUpdateResponse)

    @pytest.mark.skip(reason="400 Error: Bad Request for url: https://api.tellix.no/web/v3/vatrate/list")
    def test_var_rate_list_all(self):
        response = self.api.vat_rate_list_all(path_params=dto.OffsetLimitFromDateSortOrderPathParams())
        assert isinstance(response, dto.VATRateListAllResponse)

    def test_vat_rate_create_or_update(self):
        vat_rate = dto.VATRateCreateOrUpdateRequestBody(
            data=[dto.VATRate(vatRateId=1, vatRateTitle="Test VAT rate 1", vatRatePercent=25, isDefault=False)]
        )
        response = self.api.vat_rate_create_or_update(body=vat_rate)
        assert isinstance(response, dto.VATRateCreateOrUpdateResponse)

    def test_view_product_vat_rate_details(self):
        response = self.api.vat_rate_view_details(path_params=dto.VatRateIdPathParams(vatRateId=1))
        assert isinstance(response, dto.VATRateViewDetailsResponse)
