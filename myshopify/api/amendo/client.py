from __future__ import annotations

from typing import Dict, Optional

from apiclient.authentication_methods import BaseAuthenticationMethod
from apiclient.client import APIClient
from apiclient_pydantic import serialize_all_methods

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

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
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

        self._token = dto.AccessToken(**response.get_json()).token


@serialize_all_methods()
class AmendoAPIClient(APIClient):
    """
    https://github.com/MikeWooster/api-client
    https://api.tellix.no/api/doc
    https://tellixprotouch.docs.apiary.io/
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
        return self.post(Endpoints.generate_token, body.dict())

    """ Brand """

    def list_all_brands(self, path_params: dto.OffsetLimitFromDatePathParams) -> dto.BrandList:
        """List all brands"""
        return self.get(Endpoints.list_all_brands.format(**path_params.dict()))

    def create_brand(self, body: dto.BrandCreateBody) -> dto.BrandCreateResponse:
        return self.post(Endpoints.create_or_update_brand, body.dict())

    def update_brand(self, body: dto.BrandUpdateBody) -> dto.BrandUpdateResponse:
        """Update a brand"""
        return self.post(Endpoints.create_or_update_brand, body.dict())

    def view_brand_details(self, path_params: dto.BrandIdPathParams) -> dto.BrandViewResponse:
        """View a brands details"""
        return self.get(Endpoints.view_a_brands_details.format(**path_params.dict()))

    """ Product Category """

    def list_all_product_categories(
        self, path_params: dto.OffsetLimitFromDateSortOrderPathParams
    ) -> dto.CategoryListResponse:
        """List all product categories"""
        return self.get(Endpoints.list_all_product_categories.format(**path_params.dict()))

    def create_category(self, body: dto.CategorySavePostRequest) -> dto.CategorySaveResponse:
        """Update a category"""
        return self.post(Endpoints.create_or_update_category, body.dict())

    def update_a_category(self, body: dto.CategorySavePostRequest) -> dto.CategorySaveResponse:
        """Update a category"""
        return self.post(Endpoints.create_or_update_category, body.dict())

    def view_a_product_categorys_details(self, path_params: dto.CategoryIdPathParams) -> dto.CategoryDetails:
        """View a product categorys details"""
        return self.get(Endpoints.view_product_category_details.format(**path_params.dict()))

    """ Customer """

    def list_all_customers(self, path_params: dto.OffsetLimitPathParams) -> dto.CustomerList:
        """List all customers"""
        return self.get(Endpoints.list_all_customers.format(**path_params.dict()))

    def create_a_update(self, body: dto.CustomerSavePostRequest) -> dto.CustomerSaveResponse:
        """Create a customer"""
        return self.post(Endpoints.update_a_customer, body.dict())

    def update_a_customer(self, body: dto.CustomerSavePostRequest) -> dto.CustomerSaveResponse:
        """Update a customer"""
        return self.put(Endpoints.update_a_customer, body.dict())

    def view_a_customers_detail(self, path_params: dto.CustomerIdPathParams) -> None:
        """View a customers detail"""
        return self.get(Endpoints.view_a_customers_detail.format(**path_params.dict()))

    """ Department """

    def list_all_departments(self, path_params: dto.OffsetLimitFromDatePathParams) -> None:
        """List all departments"""
        return self.get(Endpoints.list_all_departments.format(**path_params.dict()))

    def view_a_department(self, parth_params: dto.DepartmentIdPathParams) -> dto.Department:
        return self.get(Endpoints.view_a_department.format(**parth_params.dict()))

    """ Orders """

    def list_all_orders(self, path_params: dto.OffsetLimitFromDatePathParams) -> None:
        """List all orders"""
        return self.get(Endpoints.list_all_orders.format(**path_params.dict()))

    def create_new_order_in_backoffice(self) -> None:
        """Create new order in backoffice"""
        return self.post(Endpoints.create_new_order_in_backoffice)

    def view_an_order_details(self, path_params: dto.OrderNumberPathParams) -> None:
        """View an order details"""
        return self.get(Endpoints.view_an_order_details.format(**path_params.dict()))

    def view_an_orders_detail(self, path_params: dto.IdPathParams) -> None:
        """View an orders detail"""
        return self.get(Endpoints.view_an_orders_detail.format(**path_params.dict()))

    """ Product Orders """

    """ Product stock """

    def adjust_product_stock(self, body: dto.StockAdjustPostRequest = None) -> None:
        """Adjust product stock"""
        return self.post(Endpoints.adjust_product_stock, body.dict())

    def fetch_products_stock(self, path_params: dto.ProductIdDepartmentIdPathParams) -> None:
        """Fetch products stock"""
        return self.get(Endpoints.fetch_products_stock.format(**path_params.dict()))

    def set_product_stock(self, body: dto.StockSetPostRequest = None) -> None:
        """Set product stock"""
        return self.post(Endpoints.set_product_stock, body.dict())

    """ Products """

    def list_all_product(self, path_params: myshopify.dto.amendo.params.ProductFilter, body: float = None) -> None:
        """List all product"""
        return self.get(Endpoints.list_all_product.format(**path_params.dict()), body)

    def update_a_product(self) -> None:
        """Update a product"""
        return self.post(Endpoints.update_a_product)

    def view_a_products_detail(self, path_params: dto.ProductIdPathParams) -> None:
        """View a products detail"""
        return self.get(Endpoints.view_a_products_detail.format(**path_params.dict()))

    """ Reports """

    def list_all_z_reports(self, path_params: dto.OffsetLimitPathParams) -> None:
        """List all z-reports"""
        return self.get(Endpoints.list_all_z_reports.format(**path_params.dict()))

    """ Sales Report """

    """ Suppliers """

    def list_all_suppliers(self, path_params: dto.OffsetLimitFromDatePathParams) -> None:
        """List all suppliers"""
        return self.get(Endpoints.list_all_suppliers.format(**path_params.dict()))

    def update_a_supplier(self, body: dto.SupplierSavePostRequest = None) -> None:
        """Update a supplier"""
        return self.post(Endpoints.update_a_supplier, body.dict())

    def view_a_suppliers_details(self, path_params: dto.SupplierIdPathParams) -> None:
        """View a suppliers details"""
        return self.get(Endpoints.view_a_suppliers_details.format(**path_params.dict()))

    """ Variant Group """

    """ VAT rate """

    def list_all_vat_rates(self, path_params: dto.OffsetLimitFromDatePathParams) -> None:
        """List all VAT rates"""
        return self.get(Endpoints.list_all_vat_rates.format(**path_params.dict()))

    def create_new_vat_rate(self, body: dto.VatrateSavePostRequest = None) -> None:
        """Create new VAT rate"""
        return self.post(Endpoints.create_new_vat_rate, body.dict())

    def update_a_vat_rate(self, body: dto.VatrateSavePutRequest = None) -> None:
        """Update a VAT rate"""
        self.put(Endpoints.update_a_vat_rate, body.dict())

    def view_a_vat_rates_details(self, path_params: dto.VatRateIdPathParams) -> None:
        """View a VAT rates details"""
        return self.get(Endpoints.view_a_vat_rates_details.format(**path_params.dict()))
