import pytest

import myshopify.dto.amendo as dto
from myshopify.api.amendo.client import AmendoAPIClient


class TestAmendoAPIClient:
    def setup_class(self):
        self.api = AmendoAPIClient()

    @pytest.mark.integtest
    def test_auth(self):
        response = self.api._authentication_method.get_headers()
        assert "Authorization" in response.keys()

    def test_list_all_brands(self):
        response = self.api.list_all_brands(path_params=dto.OffsetLimitFromDatePathParams())
        assert isinstance(response, dto.BrandList)

    def test_create_new_brand(self):
        brand = dto.Brand(brandName="MyBrand")
        response = self.api.create_brand(body=dto.BrandCreateBody(data=[brand]))
        assert isinstance(response, dto.BrandCreateResponse)

    def test_view_brand_details(self):
        response = self.api.view_brand_details(path_params=dto.BrandIdPathParams(brandId=1))
        assert isinstance(response, dto.BrandViewResponse)

    def test_update_brand(self):
        brand = dto.Brand(brandId=1, brandName="MyBrand")
        response = self.api.update_brand(body=dto.BrandUpdateBody(data=[brand]))
        assert isinstance(response, dto.BrandUpdateResponse)
