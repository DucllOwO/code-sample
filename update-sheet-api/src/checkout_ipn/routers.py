from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from src.database import get_db
import requests
from .schemas import PaymentCallbackBody, GetOrderHistoryByMerchantID, SendMessageToZaloBody
from .services import CheckoutIPNService, CallbackHistoryService
from ..utils import logging
from src.exceptions import DetailedHTTPException
from .constants import CallbackStatus
from typing import Optional
import traceback
router = APIRouter()

logger = logging.getLogger(__name__)


@router.post('/webhook', status_code=status.HTTP_204_NO_CONTENT)
async def update_status(body: PaymentCallbackBody, db: Session = Depends(get_db)):
    try:
        logger.debug("Webhook body: {0}".format(body))
        with db.begin():
            CheckoutIPNService.handle_webhook(body, db)
    except DetailedHTTPException as client_err:
        logger.info("Client error occurred: {0}".format(client_err.detail))
        raise client_err
    except requests.exceptions.HTTPError as http_err:  # error raise when calling with request library
        logger.info('HTTP error occurred: {0}'.format(http_err))
        raise http_err
    except Exception as err:
        traceback.print_exc()
        logger.info('Other error occurred: {0}'.format(err))
        raise err


@router.get("/history/merchant-id/{merchant_id}", response_model=list[GetOrderHistoryByMerchantID])
async def get_checkout_history(
        merchant_id: str,
        order_id: list[str] = Query(None),  # can pass many order id
        payment_status: Optional[CallbackStatus] = CallbackStatus.Successfully,
        spreadsheet_id: Optional[str] = None,
        db: Session = Depends(get_db)):
    try:
        logger.debug(order_id)
        history_list = CallbackHistoryService.get_history_by_merchant_id(
            merchant_id, payment_status, db, order_id, spreadsheet_id)
        result = [GetOrderHistoryByMerchantID.model_validate(
            temp) for temp in history_list]
        return result
    except Exception as e:
        raise e


@router.post("/notify/zalo", status_code=status.HTTP_204_NO_CONTENT)
async def send_message_to_zalo(body: SendMessageToZaloBody):
    try:
        CheckoutIPNService.send_notify_to_zalo(body)
    except requests.exceptions.HTTPError as http_err:  # error raise when calling with request library
        logger.error('HTTP error occurred: {0}'.format(http_err))
    except Exception as e:
        raise e
