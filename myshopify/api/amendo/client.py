from __future__ import annotations

from typing import Dict, Optional

from apiclient.authentication_methods import BaseAuthenticationMethod
from apiclient.client import APIClient

import myshopify.dto.amendo as dto
import myshopify.dto.amendo.params
from myshopify.api.amendo.endpoints import Endpoints
from myshopify.config import config


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

        headers = {"Content-Type": "application/x-www-form-urlencoded", "Source": "Quiltefryd AS"}
        if self._token:
            headers.update({"Authorization": self._token})
        if self._extra:
            headers.update(self._extra)
        return headers

    def perform_initial_auth(self, client: APIClient):
        response = client.post(
            Endpoints.generate_token,
            headers=self.get_headers(),
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

    def category_view_details(
        self, path_params: myshopify.dto.amendo.params.CategoryIdPathParams
    ) -> dto.CategoryDetailResponse:
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

    def customer_update_by_id(self, body: dto.CustomerSavePostRequest, customer_id: int) -> dto.BaseResponse:
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
        r = self.get(Endpoints.order_view_details_by_id.format(id=path_params.Id))
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

    def product_stock_adjust(self, body: dto.ProductStockAdjustPostRequest) -> dto.ProductStockAdjustResponse:
        """Adjust product stock"""
        r = self.post(Endpoints.product_stock_adjust, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductStockAdjustResponse(**r.json())

    def product_stock_view(self, path_params: dto.ProductIdDepartmentIdPathParams) -> dto.BaseReponse:
        """Fetch products stock"""
        r = self.get(Endpoints.product_stock_view, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductStockResponse(**r.json())

    def product_stock_set(self, body: dto.StockSetPostRequest) -> dto.BaseReponse:
        """Set product stock"""
        r = self.post(Endpoints.product_stock_set, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductStockUpdateResponse(**r.json())

    def product_stock_update(self, body: dto.StockSetPostRequest) -> dto.BaseReponse:
        """Set product stock"""
        r = self.post(Endpoints.product_stock_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductStockUpdateResponse(**r.json())

    def product_stock_module_status(self, body: dto.StockSetPostRequest) -> dto.BaseReponse:
        """Set product stock"""
        r = self.post(Endpoints.product_stock_module_status, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductStockUpdateResponse(**r.json())

    """ Products """

    def list_all_product(self, path_params: myshopify.dto.amendo.params.ProductFilter) -> dto.BaseReponse:
        """List all product"""
        r = self.get(Endpoints.product_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductListResponse(**r.json())

    def update_product(self) -> dto.BaseReponse:
        """Update a product"""
        r = self.post(Endpoints.product_create_or_update)
        r.raise_for_status()
        return dto.ProductUpdateRespose(**r.json())

    def view_products_detail(self, path_params: myshopify.dto.amendo.params.ProductIdPathParams) -> dto.BaseReponse:
        """View a products detail"""
        r = self.get(Endpoints.product_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ProductDetailResponse(**r.json())

    """ Reports """

    def list_all_z_reports(self, path_params: dto.OffsetLimitPathParams) -> dto.BaseReponse:
        """List all z-reports"""
        r = self.get(Endpoints.report_list_all_z, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.ReportsResponse(**r.json())

    """ Sales Report """

    """ Suppliers """

    def list_all_suppliers(self, path_params: dto.OffsetLimitFromDatePathParams) -> dto.BaseReponse:
        """List all suppliers"""
        r = self.get(Endpoints.supplier_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SupplierListResponse(**r.json())

    def update_supplier(self, body: dto.SupplierSavePostRequest) -> dto.BaseReponse:
        """Update a supplier"""
        r = self.post(Endpoints.supplier_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SupplierUpdateResponse(**r.json())

    def view_suppliers_details(self, path_params: myshopify.dto.amendo.params.SupplierIdPathParams) -> dto.BaseReponse:
        """View a suppliers details"""
        r = self.get(Endpoints.supplier_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.SupplierDetailResponse(**r.json())

    """ Variant Group """

    """ VAT rate """

    def list_all_vat_rates(self, path_params: dto.OffsetLimitFromDatePathParams) -> dto.BaseReponse:
        """List all VAT rates"""
        r = self.get(Endpoints.var_rate_list_all, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.VATListAllRatesResponse(**r.json())

    def create_new_vat_rate(self, body: dto.VatrateSavePostRequest) -> dto.BaseReponse:
        """Create new VAT rate"""
        r = self.post(Endpoints.vat_rate_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.VARNewRateResponse(**r.json())

    def update_vat_rate(self, body: dto.VatrateSavePutRequest) -> dto.BaseReponse:
        """Update a VAT rate"""
        r = self.put(Endpoints.vat_rate_create_or_update, data=body.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.VARUpdatRateResponse(**r.json())

    def view_vat_rates_details(self, path_params: myshopify.dto.amendo.params.VatRateIdPathParams) -> dto.BaseReponse:
        """View a VAT rates details"""
        r = self.get(Endpoints.var_rate_view_details, params=path_params.dict(exclude_unset=True))
        r.raise_for_status()
        return dto.VATRateDetailResponse(**r.json())
