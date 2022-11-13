from unittest.mock import MagicMock, patch

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
        response = self.api.list_all_brands(
            path_params=dto.OffsetLimitFromDatePathParams(from_date="2020-01-01", offset=0, limit=100)
        )
        assert isinstance(response, dto.BrandList)

    @patch("myshopify.api.amendo.client.AmendoAPIClient")
    def test_create_new_brand(self, mock_requests):
        mock_response = MagicMock()
        mock_response.return_value = dto.BrandCreateResponse(
            **{
                "status": True,
                "code": 200,
                "dateTimeBeforeQryExec": "2020-04-21 15:39:26",
                "totalAffected": 1,
                "data": [
                    {
                        "status": True,
                        "code": 200,
                        "brandData": {
                            "brandId": 15,
                            "brandName": "brand name",
                            "isActive": True,
                            "isDeleted": False,
                            "createdAt": "2020-04-21 15:39:26",
                            "updatedAt": "2020-04-21 15:39:26",
                        },
                        "validationMessage": [],
                    }
                ],
            }
        )
        mock_requests.post.return_value = mock_response
        brand = dto.Brand(brandId=1, brandName="MyBrand")
        response = self.api.create_brand(body=dto.BrandCreateBody(data=[brand]))
        assert isinstance(response, dto.BrandCreateResponse)

    def test_view_brand_details(self):
        response = self.api.view_brand_details(path_params=dto.BrandIdPathParams(brandId=1))
        assert isinstance(response, dto.BrandViewResponse)

    def test_update_brand(self):
        brand = dto.Brand(brandId=1, brandName="MyBrand")
        response = self.api.update_brand(body=dto.BrandUpdateBody(data=[brand]))
        assert isinstance(response, dto.BrandUpdateResponse)

    def test_list_all_categories(self):
        response = self.api.list_all_product_categories(
            path_params=dto.OffsetLimitFromDateSortOrderPathParams(sort_order=dto.SortOrder.ASC)
        )
        assert isinstance(response, dto.CategoryListResponse)

    def test_create_new_category(self):
        category = dto.Category(categoryName="My Category")
        response = self.api.create_category(body=dto.CategoryCreateBody(data=[category]))
        assert isinstance(response, dto.CategoryCreateResponse)

    def test_view_product_category_details(self):
        response = self.api.view_product_category_details(path_params=dto.CategoryIdPathParams())
        assert isinstance(response, dto.CategoryDetailResponse)

    def test_update_category(self):
        category = dto.Category(categoryId=1, categoryName="Mycategory")
        response = self.api.update_category(body=dto.CategoryCreateBody(data=[category]))
        assert isinstance(response, dto.CategorySaveResponse)
