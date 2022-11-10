from __future__ import annotations

from pydantic import BaseModel


class OrderNumberPathParams(BaseModel):
    orderNumber: int
