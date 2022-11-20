from __future__ import annotations

from typing import Any, List

from myshopify.dto.amendo.base import BaseResponse


class ZReportResponse(BaseResponse):
    data: List[Any]


class SalesReportResponse(BaseResponse):
    data: List[Any]
