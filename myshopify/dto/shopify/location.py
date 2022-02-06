from datetime import datetime
from typing import Optional

import shopify
from pydantic import BaseModel


class Location(BaseModel):

    # Read-only
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    id: int
    legacy: bool
    active: bool
    address1: str
    address2: str
    city: str
    country: str
    country_code: str
    name: str
    phone: str
    province: str
    province_code: str
    zip: str
    localized_country_name: str
    localized_province_name: str

    def to_shopify_object(self, existing_object: Optional[shopify.Location] = None) -> shopify.Location:
        if existing_object:
            obj = existing_object
        else:
            obj = shopify.Location()
        for field in self.__fields__:
            if self.__getattribute__(field) is not None:
                obj.__setattr__(field, self.__getattribute__(field))
        return obj

    @classmethod
    def from_shopify_object(cls, shopify_obj: shopify.Location):
        data = {}
        for field in cls.fields:
            data[field] = shopify_obj.__getattribute__(field)
        return cls(**data)
