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
        r = self.post(Endpoints.generate_token, body.dict())
        r.raise_for_status()
        return r

    """ Brand """

    def create_brand(self, body: dto.BrandCreateBody) -> dto.BrandCreateResponse:
        r = self.post(Endpoints.create_or_update_brand, body.dict())
        r.raise_for_status()
        return dto.BrandCreateResponse(**r.json())

    def update_brand(self, body: dto.BrandUpdateBody) -> dto.BrandUpdateResponse:
        """Update a brand"""
        r = self.post(Endpoints.create_or_update_brand, body.dict())
        r.raise_for_status()
        return dto.BrandUpdateResponse(**r.json())

    def list_all_brands(self, path_params: dto.OffsetLimitFromDatePathParams) -> dto.BrandList:
        """List all brands"""
        r = self.get(Endpoints.list_all_brands.format(**path_params.dict()))
        r.raise_for_status()
        return dto.BrandList(**r.json())

    def view_brand_details(self, path_params: dto.BrandIdPathParams) -> dto.BrandViewResponse:
        """View a brands details"""
        r = self.get(Endpoints.view_brands_details.format(**path_params.dict()))
        r.raise_for_status()
        return dto.BrandViewResponse(**r.json())

    """ Product Category """

    def create_category(self, body: dto.CategoryCreateBody) -> dto.CategorySaveResponse:
        """Update a category"""
        r = self.post(Endpoints.create_or_update_category, body.dict())
        r.raise_for_status()
        return dto.CategorySaveResponse(**r.json())

    def update_category(self, body: dto.CategoryCreateBody) -> dto.CategorySaveResponse:
        """Update a category"""
        r = self.post(Endpoints.create_or_update_category, body.dict())
        r.raise_for_status()
        return dto.CategorySaveResponse(**r.json())

    def list_all_product_categories(
        self, path_params: dto.OffsetLimitFromDateSortOrderPathParams
    ) -> dto.CategoryListResponse:
        """List all product categories"""
        r = self.get(Endpoints.list_all_product_categories.format(**path_params.dict()))
        r.raise_for_status()
        return dto.CategoryListResponse(**r.json())

    def view_product_category_details(self, path_params: dto.CategoryIdPathParams) -> dto.CategoryDetailResponse:
        """View a product categorys details"""
        r = self.get(Endpoints.view_product_category_details.format(**path_params.dict()))
        r.raise_for_status()
        return dto.CategoryDetailResponse(**r.json())

    """ Customer """

    def list_all_customers(self, path_params: dto.OffsetLimitPathParams) -> dto.CustomerList:
        """List all customers"""
        r = self.get(Endpoints.list_all_customers.format(**path_params.dict()))
        r.raise_for_status()
        return dto.CustomerList(**r.json())

    def create_update(self, body: dto.CustomerSavePostRequest) -> dto.CustomerSaveResponse:
        """Create a customer"""
        r = self.post(Endpoints.update_customer, body.dict())
        r.raise_for_status()
        return dto.CustomerSaveResponse(**r.json())

    def update_customer(self, body: dto.CustomerSavePostRequest) -> dto.CustomerSaveResponse:
        """Update a customer"""
        r = self.put(Endpoints.update_customer, body.dict())
        r.raise_for_status()
        return dto.CustomerSaveResponse(**r.json())

    def view_customers_detail(self, path_params: dto.CustomerIdPathParams) -> None:
        """View a customers detail"""
        r = self.get(Endpoints.view_customers_detail.format(**path_params.dict()))
        r.raise_for_status()
        return dto.CustomerDetailResponse(**r.json())

    """ Department """

    def list_all_departments(self, path_params: dto.OffsetLimitFromDatePathParams) -> None:
        """List all departments"""
        r = self.get(Endpoints.list_all_departments.format(**path_params.dict()))
        r.raise_for_status()
        return dto.DepartmentListResponse(**r.json())

    def view_department(self, parth_params: dto.DepartmentIdPathParams) -> dto.Department:
        r = self.get(Endpoints.view_department.format(**parth_params.dict()))
        r.raise_for_status()
        return dto.DepartmentResponse(**r.json())

    """ Orders """

    def list_all_orders(self, path_params: dto.OffsetLimitFromDatePathParams) -> None:
        """List all orders"""
        r = self.get(Endpoints.list_all_orders.format(**path_params.dict()))
        r.raise_for_status()
        return dto.OrderListReponse(**r.json())

    def create_new_order_in_backoffice(self) -> None:
        """Create new order in backoffice"""
        r = self.post(Endpoints.create_new_order_in_backoffice)
        r.raise_for_status()
        return dto.OrderNewInBackOfficeResponse(**r.json())

    def view_an_order_details(self, path_params: dto.OrderNumberPathParams) -> None:
        """View an order details"""
        r = self.get(Endpoints.view_an_order_details.format(**path_params.dict()))
        r.raise_for_status()
        return dto.OrderDetailResponse(**r.json())

    def view_an_orders_detail(self, path_params: dto.IdPathParams) -> None:
        """View an orders detail"""
        r = self.get(Endpoints.view_an_orders_detail.format(**path_params.dict()))
        r.raise_for_status()
        return dto.OrderListDetailReponse(**r.json())

    """ Product Orders """

    """ Product stock """

    def adjust_product_stock(self, body: dto.StockAdjustPostRequest = None) -> None:
        """Adjust product stock"""
        r = self.post(Endpoints.adjust_product_stock, body.dict())
        r.raise_for_status()
        return dto.ProductStockAdjustmentresponse(**r.json())

    def fetch_products_stock(self, path_params: dto.ProductIdDepartmentIdPathParams) -> None:
        """Fetch products stock"""
        r = self.get(Endpoints.fetch_products_stock.format(**path_params.dict()))
        r.raise_for_status()
        return dto.ProductStockResponse(**r.json())

    def set_product_stock(self, body: dto.StockSetPostRequest = None) -> None:
        """Set product stock"""
        r = self.post(Endpoints.set_product_stock, body.dict())
        r.raise_for_status()
        return dto.ProductStockUpdateResponse(**r.json())

    """ Products """

    def list_all_product(self, path_params: myshopify.dto.amendo.params.ProductFilter, body: float = None) -> None:
        """List all product"""
        r = self.get(Endpoints.list_all_product.format(**path_params.dict()), body)
        r.raise_for_status()
        return dto.ProductListResponse(**r.json())

    def update_product(self) -> None:
        """Update a product"""
        r = self.post(Endpoints.update_product)
        r.raise_for_status()
        return dto.ProductUpdateRespose(**r.json())

    def view_products_detail(self, path_params: dto.ProductIdPathParams) -> None:
        """View a products detail"""
        r = self.get(Endpoints.view_products_detail.format(**path_params.dict()))
        r.raise_for_status()
        return dto.ProductDetailResponse(**r.json())

    """ Reports """

    def list_all_z_reports(self, path_params: dto.OffsetLimitPathParams) -> None:
        """List all z-reports"""
        r = self.get(Endpoints.list_all_z_reports.format(**path_params.dict()))
        r.raise_for_status()
        return dto.ReportsResponse(**r.json())

    """ Sales Report """

    """ Suppliers """

    def list_all_suppliers(self, path_params: dto.OffsetLimitFromDatePathParams) -> None:
        """List all suppliers"""
        r = self.get(Endpoints.list_all_suppliers.format(**path_params.dict()))
        r.raise_for_status()
        return dto.SupplierListResponse(**r.json())

    def update_supplier(self, body: dto.SupplierSavePostRequest = None) -> None:
        """Update a supplier"""
        r = self.post(Endpoints.update_supplier, body.dict())
        r.raise_for_status()
        return dto.SupplierUpdateResponse(**r.json())

    def view_suppliers_details(self, path_params: dto.SupplierIdPathParams) -> None:
        """View a suppliers details"""
        r = self.get(Endpoints.view_suppliers_details.format(**path_params.dict()))
        r.raise_for_status()
        return dto.SupplierDetailResponse(**r.json())

    """ Variant Group """

    """ VAT rate """

    def list_all_vat_rates(self, path_params: dto.OffsetLimitFromDatePathParams) -> None:
        """List all VAT rates"""
        r = self.get(Endpoints.list_all_vat_rates.format(**path_params.dict()))
        r.raise_for_status()
        return dto.VATListAllRatesResponse(**r.json())

    def create_new_vat_rate(self, body: dto.VatrateSavePostRequest = None) -> None:
        """Create new VAT rate"""
        r = self.post(Endpoints.create_new_vat_rate, body.dict())
        r.raise_for_status()
        return dto.VARNewRateResponse(**r.json())

    def update_vat_rate(self, body: dto.VatrateSavePutRequest = None) -> None:
        """Update a VAT rate"""
        r = self.put(Endpoints.update_vat_rate, body.dict())
        r.raise_for_status()
        return dto.VARUpdatRateResponse(**r.json())

    def view_vat_rates_details(self, path_params: dto.VatRateIdPathParams) -> None:
        """View a VAT rates details"""
        r = self.get(Endpoints.view_vat_rates_details.format(**path_params.dict()))
        r.raise_for_status()
        return dto.VATRateDetailResponse(**r.json())
