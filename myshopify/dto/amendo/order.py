from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel

from myshopify.dto.amendo.base import BaseResponse


class OrderDetails(BaseModel):
    productId: int
    productName: str
    productNumber: int
    productExcludingVatPrice: float
    productIncludingVatPrice: float
    quantity: float
    totalProductExcludingVatPrice: float
    totalProductIncludingVatPrice: float
    discount: float
    vatRatePercent: float
    totalVatAmount: float


class PaymentDetails(BaseModel):
    paymentMethodName: str
    amount: float
    paidAmount: float
    terminalOperator: str


class GiftCardInfo(BaseModel):
    giftCardNumber: int
    title: str
    amount: float
    expiryDate: datetime


class CreditNoteInfo(BaseModel):
    creditNoteNumber: int
    title: str
    amount: float
    expiryDate: datetime


class VoucherPrefillInfo(BaseModel):
    prefillValue: float


class Order(BaseModel):
    orderId: Optional[int]
    orderNumber: Optional[int]
    departmentId: Optional[int]
    departmentName: Optional[str]
    customerId: Optional[int]
    comments: Optional[str]
    isReturnOrder: Optional[bool]
    isTakeAwayOrder: Optional[bool]
    orderStatus: Optional[str]
    totalPurchasePrice: Optional[float]
    totalPriceExcludingVat: Optional[float]
    totalPriceIncludingVat: Optional[float]
    totalDiscount: Optional[float]
    roundOffAmount: Optional[float]
    totalPay: Optional[float]
    vatAmount: Optional[float]
    createdBy: Optional[str]
    reportingDate: Optional[str]
    orderDetails: Optional[List[OrderDetails]]
    paymentDetails: Optional[List[PaymentDetails]]
    giftCardInfo: Optional[List[GiftCardInfo]]
    creditNoteInfo: Optional[List[CreditNoteInfo]]
    voucherPrefillInfo: Optional[List[VoucherPrefillInfo]]


class OrderListResponse(BaseResponse):
    data: List[Order]
    totalCount: int


class OrderData(BaseModel):
    departmentId: int
    customerId: int
    comments: str
    status: str


class ProductData(BaseModel):
    productId: int
    quantity: int
    priceIncVat: float
    comments: str
    referenceComment: str


class BackOfficeOrderData(BaseModel):
    orderData: OrderData
    productData: List[ProductData]


class OrderNewInBackOfficeBody(BaseModel):
    data: List[BackOfficeOrderData]


class OrderNewInBackOfficeResponseData(BaseModel):
    status: bool
    code: int
    orderInfo: List[Order]
    validationMessage: List[Dict[str, str]]


class OrderInBackOfficeNewResponse(BaseResponse):
    totalAffected: int
    data: List[OrderNewInBackOfficeResponseData]


class OrderInBackOfficeViewDetailsResponse(BaseResponse):
    data: List[Order]


class OrderViewDetailsResponse(BaseResponse):
    data: Order
