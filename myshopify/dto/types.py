from enum import Enum


class ShopifyProductStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"


class ShopifyInventoryManagement(str, Enum):
    SHOPIFY = "shopify"
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


class ShopifyValueType(str, Enum):
    string = "string"
    integer = "integer"
    json_string = "json_string"


class ShopifyType(str, Enum):
    single_line_text_field = "single_line_text_field"
    number_integer = "number_integer"
    number_decimal = "number_decimal"
