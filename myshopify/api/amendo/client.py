from __future__ import annotations

import logging
from typing import Dict, Optional

import requests
from apiclient.authentication_methods import BaseAuthenticationMethod
from apiclient.client import APIClient
from apiclient.utils.typing import OptionalDict

import myshopify.dto.amendo as dto
from myshopify.api.amendo.endpoints import Endpoints
from myshopify.config import config

logger = logging.getLogger(__name__)


class AmendoHeaderAuthentication(BaseAuthenticationMethod):
    """Authentication provided within the header.

    Normally associated with Oauth authorization, in the format:
    "Authorization: Bearer <token>"
    """

    def __init__(
        self,
        username: str,
        password: str,
        api_key: str,
        extra: Optional[Dict[str, str]] = None,
    ):
        self._username = username
        self._password = password
        self._api_key = api_key
        self._extra = extra
        self._token: Optional[str] = None

    def get_headers(self) -> Dict[str, str]:
        """
        - Content-Type:application/x-www-form-urlencoded; charset=utf-8
        - Accept:application/json
        """

        headers = {
            "Content-Type": "application/json",
            # "Content-Type": "application/x-www-form-urlencoded",
            "Source": "Quiltefryd AS",
            "charset": "utf-8",
            "Accept": "application/json",
        }
        if self._token:
            headers.update({"Authorization": self._token})
        if self._extra:
            headers.update(self._extra)
        return headers

    def perform_initial_auth(self, client: APIClient):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Source": "Quiltefryd AS",
        }

        response = requests.post(
            Endpoints.generate_token,
            headers=headers,
            data=dto.GetAccessTokenPostRequest(
                username=self._username,
                password=self._password,
                apikey=self._api_key,
            ).dict(),
        )

        self._token = dto.AccessToken(**response.json()).token


class AmendoAPIClient(APIClient):
    """
    https://api.tellix.no/api/doc
    https://tellixprotouch.docs.apiary.io/ (Old)

    Questions:
        Need example of product image upload using REST API
        Need all product attributes for REST API
        How to couple product with department using REST API
    """

    def __init__(self, *args, **kwargs):

        super().__init__(
            authentication_method=AmendoHeaderAuthentication(
                username=config.AMENDO_USERNAME,
                password=config.AMENDO_PASSWORD,
                api_key=config.AMENDO_API_KEY,
            ),
            *args,
            **kwargs,
        )

    def post(self, endpoint: str, data: dict, params: OptionalDict = None, **kwargs):
        """Send data and return response data from POST endpoint."""
        logger.debug("POST %s with %s", endpoint, data)
        return self.get_request_strategy().post(endpoint, json=data, data=None, params=params, **kwargs)

    def put(self, endpoint: str, data: dict, params: OptionalDict = None, **kwargs):
        """Send data to overwrite resource and return response data from PUT endpoint."""
        logger.debug("PUT %s with %s", endpoint, data)
        return self.get_request_strategy().put(endpoint, json=data, data=None, params=params, **kwargs)

    def patch(self, endpoint: str, data: dict, params: OptionalDict = None, **kwargs):
        """Send data to update resource and return response data from PATCH endpoint."""
        logger.debug("PATCH %s with %s", endpoint, data)
        return self.get_request_strategy().patch(endpoint, json=data, data=None, params=params, **kwargs)

    """ Auth """

    def generate_token(self, body: dto.GetAccessTokenPostRequest = None) -> None:
        """Generate token"""
        r = self.post(Endpoints.generate_token, body.dict())
        r.raise_for_status()
        return r

    """ Brand """

    def brand_list_all(self, path_params: dto.OffsetLimitFromDatePathParams) -> dto.BrandList:
        """List all brands"""
        r = self.get(Endpoints.brand_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.BrandList(**r.json())

    def brand_create_or_update(self, body: dto.BrandCreateBody) -> dto.BrandCreateResponse:
        r = self.post(Endpoints.brand_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.BrandCreateResponse(**r.json())

    def brand_view_details(self, path_params: dto.BrandIdPathParams) -> dto.BrandViewResponse:
        """View a brands details"""
        r = self.get(Endpoints.brand_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.BrandViewResponse(**r.json())

    """ Product Category """

    def category_list_all(self, path_params: dto.OffsetLimitFromDateSortOrderPathParams) -> dto.CategoryListResponse:
        """List all product categories"""
        r = self.get(Endpoints.product_category_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.CategoryListResponse(**r.json())

    def category_create_or_update(self, body: dto.CategoryCreateBody) -> dto.CategorySaveResponse:
        """Update a category"""
        r = self.post(Endpoints.product_category_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.CategorySaveResponse(**r.json())

    def category_view_details(self, path_params: dto.CategoryIdPathParams) -> dto.CategoryDetailResponse:
        """View a product categorys details"""
        r = self.get(Endpoints.product_category_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.CategoryDetailResponse(**r.json())

    """ Customer """

    def customer_list_all(self, path_params: dto.OffsetLimitFromDateSortOrderPathParams) -> dto.CustomerList:
        """List all customers"""
        r = self.get(Endpoints.customer_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.CustomerList(**r.json())

    def customer_create_or_update(self, body: dto.CustomerSavePostRequest) -> dto.CustomerSaveResponse:
        """Create a customer"""
        r = self.post(Endpoints.customer_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.CustomerSaveResponse(**r.json())

    def customer_update_by_id(self, body: dto.CustomerUpdatePostRequest, customer_id: int) -> dto.BaseResponse:
        """Update a customer"""
        r = self.put(Endpoints.customer_update_by_id.format(id=customer_id), data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.CustomerSaveResponse(**r.json())

    def customer_view_details(self, path_params: dto.CustomerIdPathParams) -> dto.CustomerViewResponse:
        """View a customer's details"""
        r = self.get(Endpoints.customer_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.CustomerViewResponse(**r.json())

    """ Department """

    def department_view_info(self, parth_params: dto.DepartmentIdPathParams) -> dto.DepartmentViewResponse:
        r = self.get(Endpoints.department_view_info, params=parth_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.DepartmentViewResponse(**r.json())

    def department_list_all(self, path_params: dto.OffsetLimitFromDatePathParams) -> dto.DepartmentListResponse:
        """List all departments"""
        r = self.get(Endpoints.department_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.DepartmentListResponse(**r.json())

    """ Orders """

    def order_list_all(self, path_params: dto.OffsetLimitFromDateSortOrderPathParams) -> dto.OrderListResponse:
        """
        List all orders

        Todo: Investigated: Somehow the response dateTimeBeforeQryExec is formatted YYYY/MM/DD HH:MM:SS
        """
        r = self.get(Endpoints.order_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.OrderListResponse(**r.json())

    def order_create_new_in_back_office(self, body: dto.OrderNewInBackOfficeBody) -> dto.OrderInBackOfficeNewResponse:
        """Create new order in backoffice"""
        r = self.post(Endpoints.order_in_back_office_create, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.OrderInBackOfficeNewResponse(**r.json())

    def order_in_back_office_view_details(
        self, path_params: dto.OrderNumberPathParams
    ) -> dto.OrderInBackOfficeViewDetailsResponse:
        """Create new order in backoffice"""
        r = self.get(Endpoints.order_in_back_office_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.OrderInBackOfficeViewDetailsResponse(**r.json())

    def order_view_details_by_id(self, path_params: dto.IdPathParams) -> dto.OrderViewDetailsResponse:
        """View an orders detail"""
        r = self.get(Endpoints.order_view_details_by_id.format(id=path_params.id))
        r.raise_for_status()
        return dto.OrderViewDetailsResponse(**r.json())

    """ Product Orders """

    def products_order_info(
        self, path_params: dto.OrderStatusLimitOffsetOrderByParams
    ) -> dto.ProductsOrderInfoResponse:
        r = self.get(Endpoints.products_order_info, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductsOrderInfoResponse(**r.json())

    """ Product stock """

    def product_stock_all_products_info(
        self, body: dto.StockAllProductInfoRequestBody
    ) -> dto.StockAllProductInfoResponseBody:
        """Adjust product stock"""
        r = self.post(Endpoints.product_stock_list_all, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.StockAllProductInfoResponseBody(**r.json())

    def product_stock_add(
        self, body: dto.ProductStockAddRequestBody, path_params: dto.ProductIdOrderIdPathParams
    ) -> dto.ProductStockAddResponse:
        """Adjust product stock"""
        r = self.post(
            Endpoints.product_stock_add_receive,
            data=body.dict(exclude_unset=True),
            params=path_params.dict(exclude_unset=True),
        )
        r.raise_for_status()
        return dto.ProductStockAddResponse(**r.json())

    def product_stock_adjust(
        self, body: dto.ProductStockAdjustPostRequest, product_id: int
    ) -> dto.ProductStockAdjustResponse:
        """Adjust product stock"""
        r = self.post(Endpoints.product_stock_adjust, data=body.dict(exclude_unset=True), params={"id": product_id})
        r.raise_for_status()
        return dto.ProductStockAdjustResponse(**r.json())

    def product_stock_view(self, path_params: dto.IdPathParams) -> dto.ProductStockAdjustResponse:
        """Fetch products stock"""
        r = self.get(Endpoints.product_stock_view, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductStockAdjustResponse(**r.json())

    def product_stock_set(
        self, body: dto.ProductStockSetPostRequest, product_id: int
    ) -> dto.ProductStockAdjustResponse:
        """Set product stock"""
        r = self.post(Endpoints.product_stock_set, data=body.dict(exclude_unset=True), params={"id": product_id})
        r.raise_for_status()
        return dto.ProductStockAdjustResponse(**r.json())

    def product_stock_update(self, body: dto.ProductStockUpdateRequestBody) -> None:
        """Set product stock"""
        r = self.post(Endpoints.product_stock_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        pass

    def product_stock_module_status(self) -> dto.BaseResponse:
        """Set product stock"""
        r = self.post(Endpoints.product_stock_module_status, data={})
        r.raise_for_status()
        return dto.BaseResponse(**r.json())

    """ Products """

    def product_list_all(self, path_params: dto.ProductFilter) -> dto.ProductListResponse:
        """List all product"""
        r = self.get(Endpoints.product_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductListResponse(**r.json())

    def product_create_or_update(self, body: dto.ProductCreateOrUpdateRequestBody) -> dto.ProductPostResponse:
        """Update a product"""
        r = self.post(Endpoints.product_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductPostResponse(**r.json())

    def product_update_by_id(self, body: dto.ProductUpdateByIdRequestBody, product_id: int) -> dto.BaseResponse:
        """Update a product"""
        r = self.put(Endpoints.product_update_by_id.format(id=product_id), data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.BaseResponse(**r.json())

    def product_update_updated_at(self):
        """https://api.tellix.no/api/doc#patch--web-{version}-product-updateUpdatedAt"""
        raise NotImplementedError("Update UpdateAt has not been implemented")

    def product_variant_create_or_update(
        self, body: dto.ProductVariantCreateOrUpdateRequestBody
    ) -> dto.ProductVariantPostResponse:
        """Update a product"""
        r = self.post(Endpoints.product_variant_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductVariantPostResponse(**r.json())

    def product_view_details(self, path_params: dto.ProductIdPathParams) -> dto.BaseResponse:
        """View a products detail"""
        r = self.get(Endpoints.product_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductDetailResponse(**r.json())

    """ Reports """

    def report_list_all_z(self, path_params: dto.OffsetLimitPathParams) -> dto.BaseResponse:
        """List all z-reports"""
        r = self.get(Endpoints.report_list_all_z, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ZReportResponse(**r.json())

    """ Sales Report """

    def report_sales(self, path_params: dto.OffsetLimitPathParams) -> dto.BaseResponse:
        """Report sales"""
        r = self.get(Endpoints.sales_report_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SalesReportResponse(**r.json())

    """ Suppliers """

    def supplier_list_all(self, path_params: dto.OffsetLimitFromDateSortOrderPathParams) -> dto.SupplierListAllResponse:
        """List all suppliers"""
        r = self.get(Endpoints.supplier_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SupplierListAllResponse(**r.json())

    def supplier_create_or_update(self, body: dto.SupplierCreateOrUpdateBody) -> dto.SupplierCreateOrUpdateResponse:
        """Update a supplier"""
        r = self.post(Endpoints.supplier_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SupplierCreateOrUpdateResponse(**r.json())

    def supplier_view_details(self, path_params: dto.SupplierIdPathParams) -> dto.SupplierViewDetailsResponse:
        """View a suppliers details"""
        r = self.get(Endpoints.supplier_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SupplierViewDetailsResponse(**r.json())

    """ Variant Group """

    def variant_group_list_all(
        self, path_params: dto.OffsetLimitFromDateSortOrderPathParams
    ) -> dto.SupplierViewDetailsResponse:
        """List all variant_groups"""
        r = self.get(Endpoints.variant_group_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SupplierViewDetailsResponse(**r.json())

    def variant_group_create_or_update(self, body: dto.SupplierViewDetailsResponse) -> dto.SupplierViewDetailsResponse:
        """Update a variant_group"""
        r = self.post(Endpoints.variant_group_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SupplierViewDetailsResponse(**r.json())

    """ VAT rate """

    def var_rate_list_all(self, path_params: dto.OffsetLimitFromDatePathParams) -> dto.BaseResponse:
        """List all VAT rates"""
        r = self.get(Endpoints.var_rate_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.VATListAllRatesResponse(**r.json())

    def vat_rate_create_or_update(self, body: dto.VatrateSavePostRequest) -> dto.BaseResponse:
        """Create new VAT rate"""
        r = self.post(Endpoints.vat_rate_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.VARNewRateResponse(**r.json())

    def var_rate_view_details(self, path_params: dto.VatRateIdPathParams) -> dto.BaseResponse:
        """View a VAT rates details"""
        r = self.get(Endpoints.var_rate_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.VATRateDetailResponse(**r.json())
