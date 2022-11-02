from datetime import datetime
from typing import Dict, List, Optional

import shopify
from pydantic import BaseModel


class InventoryItem(BaseModel):

    # Read-only
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    id: int
    sku: str
    cost: str
    country_code_of_origin: str  # ISO 3166-1 alpha-2
    country_harmonized_system_codes: List[Dict[str, str]]
    harmonized_system_code: int
    province_code_of_origin: str  # ISO 3166-2 alpha-2
    tracked: bool
    requires_shipping: bool

    def to_shopify_object(self, existing_object: Optional[shopify.InventoryItem] = None) -> shopify.InventoryItem:
        if existing_object:
            obj = existing_object
        else:
            obj = shopify.InventoryItem()
        for field in self.__fields__:
            if self.__getattribute__(field) is not None:
                obj.__setattr__(field, self.__getattribute__(field))
        return obj

    @classmethod
    def from_shopify_object(cls, shopify_obj: shopify.InventoryItem):
        data = {}
        for field in cls.fields:
            data[field] = shopify_obj.__getattribute__(field)
        return cls(**data)


class InventoryLevel(BaseModel):
    # Read-only
    updated_at: Optional[datetime] = None  # read-only

    available: int
    inventory_item_id: int
    location_id: int

    def to_shopify_object(self, existing_object: Optional[shopify.InventoryLevel] = None) -> shopify.InventoryLevel:
        if existing_object:
            obj = existing_object
        else:
            obj = shopify.InventoryLevel()
        for field in self.__fields__:
            if self.__getattribute__(field) is not None:
                obj.__setattr__(field, self.__getattribute__(field))
        return obj

    @classmethod
    def from_shopify_object(cls, shopify_obj: shopify.InventoryLevel):
        data = {}
        for field in cls.fields:
            data[field] = shopify_obj.__getattribute__(field)
        return cls(**data)
