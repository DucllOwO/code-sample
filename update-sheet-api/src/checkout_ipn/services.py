from sqlalchemy.orm import Session
from src.utils import logging, convert_vn_phone_to_international
from src.spreadsheet.service import SpreadsheetService
from src.checkout_ipn.schemas import PaymentCallbackBody, MessageZaloData, SendMessageToZaloBody
from .constants import CallbackStatus
from .models import CallbackHistory
from src.exceptions import BadRequest
from src.config import settings
from src.database import dynamic_session
from typing import List, Optional
import requests

logger = logging.getLogger(__name__)


class CheckoutIPNService:
    @classmethod
    def handle_webhook(self, body: PaymentCallbackBody, db: Session):
        spreadsheet_id, sheet_id, order_id = self.decode_order_id(body.order_id)

        logger.debug("spreadsheet_id: {0}; sheet_id: {1}; order_id: {2}".format(
            spreadsheet_id, sheet_id, order_id))

        spreadsheets = SpreadsheetService.get_spreadsheet_by_merchant_id(
            body.merchant_id, spreadsheet_id, db)

        if spreadsheets is None:
            raise BadRequest(
                "This merchant has not registered google sheet information yet")

        try:
            SpreadsheetService.update_status(
                order_id, spreadsheet_id, sheet_id)
        except Exception as e:
            new_session = dynamic_session()
            with new_session.begin():
                CallbackHistoryService.save_history(
                    body, order_id, spreadsheet_id, sheet_id, CallbackStatus.UnSuccessfully.value, settings.APP_ID, new_session)
            raise e

        CallbackHistoryService.save_history(
            body, order_id, spreadsheet_id, sheet_id, CallbackStatus.Successfully.value, settings.APP_ID, db)

    @classmethod
    def decode_order_id(self, order_id_encoded: str):
        """
            The order id is built in format '<spreadsheet-id>#<sheet-id>#<some identifier that unique in the sheet = order id>'
            For example: 1Y43Gj6cgf3yxOF5smmC-MlnJTKAoZHSdYFROb7NDNsY#189324742#1
        """
        try:
            spreadsheet_id, sheet_id, order_id = order_id_encoded.split("#")
        except Exception as e:
            logger.debug(order_id_encoded)
            raise BadRequest(detail="Order ID in invalid")

        return spreadsheet_id, sheet_id, order_id

    @classmethod
    def send_notify_to_zalo(self, data: SendMessageToZaloBody):
        """

        """
        logger.debug(data.model_dump_json())

        # update phone number to international format
        for item in data.messages:
            logger.debug(convert_vn_phone_to_international(item.phone))
            item.phone = convert_vn_phone_to_international(item.phone)

        headers = {
            "origin": "edu.vitrust.app"
        }
        response = requests.post(settings.EDU_BACKEND_URL
                                 + "/zalo_zns", data=data.model_dump_json(), headers=headers)
        response.raise_for_status()


class CallbackHistoryService:
    @classmethod
    def save_history(self, payment_callback: PaymentCallbackBody, order_id: str, spreadsheet_id: str, sheet_id: str, status: CallbackStatus, app_id: str, db: Session):
        callback_history = CallbackHistory(
            merchant_id=payment_callback.merchant_id, amount=payment_callback.amount, order_id=order_id, spreadsheet_id=spreadsheet_id, sheet_id=sheet_id, status=status, app_id=app_id)

        db.add(callback_history)

        return callback_history

    @classmethod
    def get_history_by_merchant_id(
        cls,
        merchant_id: str,
        callback_status: CallbackStatus,
        db: Session,
        order_ids: Optional[List[str]] = None,
        spreadsheet_id: Optional[str] = None
    ) -> List[CallbackHistory]:
        query = db.query(CallbackHistory).filter(
            CallbackHistory.merchant_id == str(merchant_id),
            CallbackHistory.status == callback_status
        )

        if spreadsheet_id is not None:
            query = query.filter(CallbackHistory.spreadsheet_id == spreadsheet_id)

        if order_ids is not None:
            query = query.filter(CallbackHistory.order_id.in_(order_ids))

        return query.all()
