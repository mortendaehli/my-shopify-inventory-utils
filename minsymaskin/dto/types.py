from enum import Enum


class ShopifyProductStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"


class ShopifyInventoryManagement(str, Enum):
    SHOPIFY = "shopify"
    NULL = None
    FULFILLMENT_SERVICE = "fulfillment_service"


class ShopifyInventoryPolicy(str, Enum):
    DENY = "deny"
    CONTINUE = "continue"


class ShopifyWeightUnit(str, Enum):
    G = "g"
    KG = "kg"
    OZ = "oz"
    LB = "lb"


class ShopifyFulfillmentService(str, Enum):
    MANUAL = "manual"


class ShopifyPublishScope(str, Enum):
    WEB = "web"
    GLOBAL = "global"
