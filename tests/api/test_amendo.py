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

    @pytest.mark.skip(reason="This does not seem to work as of now...")
    def test_create_new_brand(self):
        brand = dto.Brand(brandId=1, brandName="Test brand", isActive=False)
        response = self.api.brand_create_or_update(body=dto.BrandCreateBody(data=[brand]))
        assert isinstance(response, dto.BrandCreateResponse)

    def test_view_brand_details(self):
        response = self.api.brand_view_details(path_params=dto.BrandIdPathParams(brandId=1))
        assert isinstance(response, dto.BrandViewResponse)

    def test_list_all_categories(self):
        response = self.api.category_list_all(
            path_params=dto.OffsetLimitFromDateSortOrderPathParams(
                sortOrder=dto.SortOrder.ASC, offset=0, limit=2, fromDate=date(2020, 1, 1)
            )
        )
        assert isinstance(response, dto.CategoryListResponse)

    @pytest.mark.skip(reason="This does not seem to work as of now...")
    def test_category_create_or_update(self):
        category = dto.Category(categoryId=1, categoryName="Test category", isActive=False)
        response = self.api.category_create_or_update(body=dto.CategoryCreateBody(data=[category]))
        assert isinstance(response, dto.CategoryCreateResponse)

    def test_view_product_category_details(self):
        response = self.api.category_view_details(path_params=dto.CategoryIdPathParams(categoryId=1))
        assert isinstance(response, dto.CategoryDetailResponse)

    def test_customer_list_all(self):
        response = self.api.customer_list_all(path_params=dto.OffsetLimitFromDateSortOrderPathParams())
        assert isinstance(response, dto.CustomerList)

    @pytest.mark.skip(reason="This does not seem to work as of now...")
    def test_customer_create_or_update(self):
        response = self.api.customer_create_or_update(
            body=dto.CustomerSavePostRequest(
                data=[dto.Customer(customerId=1, name="Test Customer", country="Norway", isActive=False)]
            )
        )
        assert isinstance(response, dto.CustomerSaveResponse)

    @pytest.mark.skip(reason="This does not seem to work as of now...")
    def test_customer_update_by_id(self):
        response = self.api.customer_update_by_id(
            customer_id=1,
            body=dto.CustomerSavePostRequest(
                data=[dto.Customer(customerId=1, name="Test Customer", country="Norway", isActive=False)]
            ),
        )
        assert isinstance(response, dto.BaseResponse)

    def test_customer_view_details(self):
        response = self.api.customer_view_details(path_params=dto.CustomerIdPathParams(customerId=1))
        assert isinstance(response, dto.CategoryDetailResponse)

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
        response = self.api.order_view_details_by_id(path_params=dto.IdPathParams(Id=1))
        assert isinstance(response, dto.OrderViewDetailsResponse)

    def test_products_order_info(self):
        response = self.api.products_order_info(path_params=dto.OrderStatusLimitOffsetOrderByParams())
        assert isinstance(response, dto.ProductsOrderInfoResponse)

    @pytest.mark.skip(reason="This does not seem to work as of now...")
    def test_product_stock_all_products_info(self):
        response = self.api.product_stock_all_products_info(
            body=dto.StockAllProductInfoRequestBody(
                params=dto.StockAllProductInfoParams(stockDepartment=1, fromDate=date(2020, 1, 1))
            )
        )
        assert isinstance(response, dto.StockAllProductInfoResponseBody)
