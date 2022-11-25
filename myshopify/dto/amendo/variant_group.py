from __future__ import annotations

from typing import List, Union

from myshopify.dto.amendo.base import BaseEntity, BaseResponse


class VariantValue(BaseEntity):
    variantValueId: int
    variantValue: Union[int, float, str]


class VariantGroupData(BaseEntity):
    variantGroupId: int
    variantGroupName: str
    variantValues: List[VariantValue]


class VariantGroupCreateOrUpdateBody(BaseEntity):
    data: VariantGroupData


class VariantGroupCreateOrUpdateResponse(BaseResponse):
    data: VariantGroupData


class VariantGroupListAllResponse(BaseResponse):
    data: List[VariantGroupData]
