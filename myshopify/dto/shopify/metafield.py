from datetime import datetime
from typing import Optional, Union

import shopify
from pydantic import BaseModel

from myshopify.dto.types import ShopifyType, ShopifyValueType


class Metafield(BaseModel):

    # Read-only
    id: Optional[int]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    description: Optional[str]
    owner_id: Optional[int]  # product id
    owner_resource: Optional[str]  # eg. product

    key: str
    namespace: str
    value: Union[int, float, str]
    type: ShopifyType
    value_type: ShopifyValueType

    def to_shopify_object(self, existing_object: Optional["Metafield"] = None) -> "Metafield":
        if existing_object:
            obj = existing_object
        else:
            obj = shopify.Metafield()
        for field in self.__fields__:
            if self.__getattribute__(field) is not None:
                obj.__setattr__(field, self.__getattribute__(field))
        return obj

    @classmethod
    def from_shopify_object(cls, shopify_obj: "Metafield"):
        data = {}
        for field in cls.fields:
            data[field] = shopify_obj.__getattribute__(field)
        return cls(**data)

    class Config:
        use_enum_values = True
