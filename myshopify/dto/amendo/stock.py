from __future__ import annotations

from datetime import date
from typing import List, Union

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseResponse


class ProductStockAddProductData(BaseModel):
    productId: int
    productCount: int


class ProductStockAddData(BaseModel):
    department_id: int
    products: List[ProductStockAddProductData]


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


class ProductStockSetPostRequestData(BaseModel):
    department_id: int
    product_id: int
    stock_quantity: int


class ProductStockAdjustPostRequest(BaseModel):
    data: ProductStockAdjustPostRequestData


class ProductStockSetPostRequest(BaseModel):
    data: ProductStockSetPostRequestData


class StockAllProductInfoParams(BaseModel):
    stockDepartment: int
    fromDate: date


class StockAllProductInfoRequestBody(BaseModel):
    params: StockAllProductInfoParams


class ProductStock(BaseModel):
    productId: int
    productNumber: int
    stockQuantity: int


class ProductStockUpdateData(BaseModel):
    stockDepartment: int
    productNumber: int
    stockQuantity: int


class ProductVariantStock(BaseModel):
    productId: int
    productNumber: int
    childProducts: List[ProductStock]


class StockAllProductInfoResponseBody(BaseResponse):
    productDetails: List[Union[ProductStock, ProductVariantStock]]


class ProductStockUpdateRequestBody(BaseModel):
    params: ProductStockUpdateData
