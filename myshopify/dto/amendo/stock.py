from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Data(BaseModel):
    adjust_stock_quantity: Optional[float] = None
    department_id: Optional[float] = None
    product_id: Optional[float] = None


class StockAdjustPostRequest(BaseModel):
    data: Optional[Data] = None


class Data1(BaseModel):
    department_id: Optional[float] = None
    product_id: Optional[float] = None
    stock_quantity: Optional[float] = None


class StockSetPostRequest(BaseModel):
    data: Optional[Data1] = None
