from src.models import ORJSONModel
from .constants import CallbackStatus, OrderStatus
from pydantic import field_validator


class PaymentCallbackBody(ORJSONModel):
    order_id: str
    merchant_id: str
    amount: int


class GetOrderHistoryByMerchantID(ORJSONModel):
    order_id: str
    sheet_id: str
    status: OrderStatus

    @field_validator('status', mode='before')
    @classmethod
    def map_status(cls, v) -> OrderStatus:
        if isinstance(v, CallbackStatus):
            # Map CallbackStatus to OrderStatus
            status_map = {
                CallbackStatus.Successfully: OrderStatus.Completed,
                CallbackStatus.UnSuccessfully: OrderStatus.InComplete
            }
            # Default to InComplete if not found
            return status_map.get(v, OrderStatus.InComplete)
        elif isinstance(v, str):
            # Handle case where input might be a string
            try:
                return OrderStatus(v)
            except ValueError:
                # If string doesn't match OrderStatus, try mapping from CallbackStatus string
                callback_status = CallbackStatus(v)
                return cls.map_status(callback_status)
        elif isinstance(v, OrderStatus):
            # If it's already OrderStatus, return as is
            return v
        else:
            raise ValueError(f"Invalid status type: {type(v)}")


class TemplateMessageData(ORJSONModel):
    Amount: str
    payment: str
    Fee_Content: str
    Student_Name: str


class MessageZaloData(ORJSONModel):
    phone: str
    template_data: TemplateMessageData


class SendMessageToZaloBody(ORJSONModel):
    messages: list[MessageZaloData]
