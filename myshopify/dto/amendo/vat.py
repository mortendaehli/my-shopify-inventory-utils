from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class VATRate(BaseEntity):
    vatRateId: int
    vatRateTitle: Optional[str]
    vatRatePercent: float
    isDefault: bool


class VATRateListAllResponse(BaseModel):
    vatRates: List[VATRate]
    totalCount: int


class VATRateCreateOrUpdateRequestBody(BaseModel):
    data: List[VATRate]


class VATRateCreateOrUpdateResponseData(BaseResponse):
    vatRateData: VATRate
    validationMessage: Any


class VATRateCreateOrUpdateResponse(BaseModel):
    data: List[VATRateCreateOrUpdateResponseData]


class VATRateViewDetailsResponse(BaseResponse):
    data: VATRate
