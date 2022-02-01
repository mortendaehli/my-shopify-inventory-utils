from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class InventoryItem(BaseModel):
    cost: str
    country_code_of_origin: str  # ISO 3166-1 alpha-2
    country_harmonized_system_codes: List[Dict[str, str]]
    created_at: Optional[datetime] = None  # read-only
    harmonized_system_code: int
    id: int
    province_code_of_origin: str  # ISO 3166-2 alpha-2
    sku: str
    tracked: bool
    updated_at: datetime
    requires_shipping: bool


class InventoryLevel(BaseModel):
    available: int
    inventory_item_id: int
    location_id: int
    updated_at: Optional[datetime] = None  # read-only


class Location(BaseModel):
    active: bool
    address1: str
    address2: str
    city: str
    country: str
    country_code: str
    created_at: Optional[datetime]
    id: int
    legacy: bool
    name: str
    phone: str
    province: str
    province_code: str
    updated_at: Optional[datetime]
    zip: str
    localized_country_name: str
    localized_province_name: str
