from __future__ import annotations

from datetime import date
from typing import List, Union

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseResponse


class ProductStockAddData(BaseModel):
    department_id: int
    products: List[ProductStock]


class ProductStockAddRequestBody(BaseModel):
    data: ProductStockAddData


class ProductStockAddResponseBody(ProductStockAddData):
    productOrderId: int


class ProductStockAddResponse(BaseModel):
    data: ProductStockAddResponseBody


class ProductStockAdjustResponse(BaseResponse):
    stockQuantity: int


class ProductStockAdjustPostRequestData(BaseModel):
    department_id: int
    product_id: int
    adjust_stock_quantity: int


class ProductStockAdjustPostRequestRequest(BaseModel):
    data: ProductStockAdjustPostRequestData


class StockAllProductInfoParams(BaseModel):
    stockDepartment: int
    fromDate: date


class StockAllProductInfoRequestBody(BaseModel):
    params: StockAllProductInfoParams


class ProductStock(BaseModel):
    productId: int
    productNumber: int
    stockQuantity: int


class ProductVariantStock(BaseModel):
    productId: int
    productNumber: int
    childProducts: List[ProductStock]


class StockAllProductInfoResponseBody(BaseResponse):
    productDetails: List[Union[ProductStock, ProductVariantStock]]
