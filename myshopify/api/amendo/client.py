from __future__ import annotations
from typing import Optional, Dict
from apiclient.client import APIClient
from apiclient.authentication_methods import BaseAuthenticationMethod
from apiclient_pydantic import serialize_all_methods

from myshopify.config import config
from myshopify.api.amendo.endpoints import Endpoints
from myshopify.api.amendo.models import (
    BrandIdPathParams,
    BrandSavePostRequest,
    CategoryIdPathParams,
    CategorySavePostRequest,
    CustomerIdPathParams,
    GetaccesstokenPostRequest,
    IdPathParams,
    OffsetLimitFromDatePathParams,
    OffsetLimitFromDateSortOrderPathParams,
    OffsetLimitPathParams,
    OrderNumberPathParams,
    ProductFilter,
    ProductIdDepartmentIdPathParams,
    ProductIdPathParams,
    StockAdjustPostRequest,
    StockSetPostRequest,
    SupplierIdPathParams,
    SupplierSavePostRequest,
    VatRateIdPathParams,
    VatrateSavePostRequest,
    VatrateSavePutRequest,
)


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
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        if self._token:
            headers.update({"Authorization": self._token})
        if self._extra:
            headers.update(self._extra)
        return headers

    def perform_initial_auth(self, client: APIClient):
        response = client.post(
            Endpoints.generate_token,
            headers=self.get_headers(),
            data=GetaccesstokenPostRequest(
                username=self._username,
                password=self._password,
                apikey=self._api_key,
            ).dict()
        )

        self._token = response.get_json()["token"]


@serialize_all_methods()
class AmendoAPIClient(APIClient):
    """
    https://github.com/MikeWooster/api-client
    https://api.tellix.no/api/doc
    https://tellixprotouch.docs.apiary.io/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(authentication_method=AmendoHeaderAuthentication(
            username=config.AMENDO_USERNAME,
            password=config.AMENDO_PASSWORD,
            api_key=config.AMENDO_API_KEY,
        ), *args, **kwargs)

    def list_all_brands(self, path_params: OffsetLimitFromDatePathParams) -> None:
        """List all brands"""
        self.get(Endpoints.list_all_brands.format(**path_params.dict()))

    def update_a_brand(self, body: BrandSavePostRequest = None) -> None:
        """Update a brand"""
        self.post(Endpoints.update_a_brand, body.dict())

    def view_a_brands_details(self, path_params: BrandIdPathParams) -> None:
        """View a brands details"""
        self.get(Endpoints.view_a_brands_details.format(**path_params.dict()))

    def list_all_product_categories(
            self, path_params: OffsetLimitFromDateSortOrderPathParams) -> None:
        """List all product categories"""
        self.get(Endpoints.list_all_product_categories.format(**path_params.dict()))

    def update_a_category(self, body: CategorySavePostRequest = None) -> None:
        """Update a category"""
        self.post(Endpoints.update_a_category, body.dict())

    def view_a_product_categorys_details(
            self, path_params: CategoryIdPathParams) -> None:
        """View a product categorys details"""
        self.get(
            Endpoints.view_a_product_categorys_details.format(**path_params.dict()))

    def list_all_customers(self, path_params: OffsetLimitPathParams) -> None:
        """List all customers"""
        self.get(Endpoints.list_all_customers.format(**path_params.dict()))

    def update_a_customer(self) -> None:
        """Update a customer"""
        self.post(Endpoints.update_a_customer)

    def view_a_customers_detail(self,
                                path_params: CustomerIdPathParams) -> None:
        """View a customers detail"""
        self.get(Endpoints.view_a_customers_detail.format(**path_params.dict()))

    def list_all_departments(
            self, path_params: OffsetLimitFromDatePathParams) -> None:
        """List all departments"""
        self.get(Endpoints.list_all_departments.format(**path_params.dict()))

    def generate_token(self, body: GetaccesstokenPostRequest = None) -> None:
        """Generate token"""
        self.post(Endpoints.generate_token, body.dict())

    def list_all_orders(self,
                        path_params: OffsetLimitFromDatePathParams) -> None:
        """List all orders"""
        self.get(Endpoints.list_all_orders.format(**path_params.dict()))

    def create_new_order_in_backoffice(self) -> None:
        """Create new order in backoffice"""
        self.post(Endpoints.create_new_order_in_backoffice)

    def view_an_order_details(self,
                              path_params: OrderNumberPathParams) -> None:
        """View an order details"""
        self.get(Endpoints.view_an_order_details.format(**path_params.dict()))

    def view_an_orders_detail(self, path_params: IdPathParams) -> None:
        """View an orders detail"""
        self.get(Endpoints.view_an_orders_detail.format(**path_params.dict()))

    def list_all_product(self, path_params: ProductFilter, body: float = None) -> None:
        """List all product"""
        self.get(Endpoints.list_all_product.format(**path_params.dict()), body)

    def update_a_product(self) -> None:
        """Update a product"""
        self.post(Endpoints.update_a_product)

    def view_a_products_detail(self, path_params: ProductIdPathParams) -> None:
        """View a products detail"""
        self.get(Endpoints.view_a_products_detail.format(**path_params.dict()))

    def adjust_product_stock(self,
                             body: StockAdjustPostRequest = None) -> None:
        """Adjust product stock"""
        self.post(Endpoints.adjust_product_stock, body.dict())

    def fetch_products_stock(
            self, path_params: ProductIdDepartmentIdPathParams) -> None:
        """Fetch products stock"""
        self.get(Endpoints.fetch_products_stock.format(**path_params.dict()))

    def set_product_stock(self, body: StockSetPostRequest = None) -> None:
        """Set product stock"""
        self.post(Endpoints.set_product_stock, body.dict())

    def list_all_suppliers(self,
                           path_params: OffsetLimitFromDatePathParams) -> None:
        """List all suppliers"""
        self.get(Endpoints.list_all_suppliers.format(**path_params.dict()))

    def update_a_supplier(self, body: SupplierSavePostRequest = None) -> None:
        """Update a supplier"""
        self.post(Endpoints.update_a_supplier, body.dict())

    def view_a_suppliers_details(self,
                                 path_params: SupplierIdPathParams) -> None:
        """View a suppliers details"""
        self.get(Endpoints.view_a_suppliers_details.format(**path_params.dict()))

    def list_all__v_a_t_rates(
            self, path_params: OffsetLimitFromDatePathParams) -> None:
        """List all VAT rates"""
        self.get(Endpoints.list_all__v_a_t_rates.format(**path_params.dict()))

    def create_new__v_a_t_rate(self,
                               body: VatrateSavePostRequest = None) -> None:
        """Create new VAT rate"""
        self.post(Endpoints.create_new__v_a_t_rate, body.dict())

    def update_a__v_a_t_rate(self, body: VatrateSavePutRequest = None) -> None:
        """Update a VAT rate"""
        self.put(Endpoints.update_a__v_a_t_rate, body.dict())

    def view_a__v_a_t_rates_details(self,
                                    path_params: VatRateIdPathParams) -> None:
        """View a VAT rates details"""
        self.get(Endpoints.view_a__v_a_t_rates_details.format(**path_params.dict()))

    def list_all_z_reports(self, path_params: OffsetLimitPathParams) -> None:
        """List all z-reports"""
        self.get(Endpoints.list_all_z_reports.format(**path_params.dict()))
