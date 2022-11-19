from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class VATRate(BaseModel):
    isActive: bool
    vatRatePercent: float


class VatrateSavePostRequest(BaseModel):
    data: Optional[List[VATRate]] = None


class Datum4(BaseModel):
    isActive: bool
    vatRateId: Optional[int]
    vatRatePercent: float


class VatrateSavePutRequest(BaseModel):
    data: Optional[List[Datum4]] = None
