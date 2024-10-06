from src.config import settings
from src.checkout_ipn.constants import OrderStatus
import requests
from sqlalchemy.orm import Session
from src.spreadsheet.models import SheetManagement
from src.spreadsheet.constants import SheetType
from src.models import PaginationParams, PaginationSchema
from sqlalchemy import func
from src.utils import logging
from typing import Optional

logger = logging.getLogger(__name__)


class SpreadsheetService:
    @classmethod
    def update_status(self, order_id: str, spreadsheet_id: str, sheet_id: str):
        response = requests.post(
            '{0}?id={1}&status={2}&spreadsheetId={3}&sheetId={4}'.format(settings.APP_SCRIPTS, order_id, OrderStatus.Completed.value, spreadsheet_id, sheet_id))
        response.raise_for_status()

    @classmethod
    def get_spreadsheets_by_merchant_id(self, merchant_id: str, db: Session, pagination_params: Optional[PaginationParams] = None) -> list[SheetManagement]:
        spreadsheets = db.query(SheetManagement).filter(
            SheetManagement.merchant_id == merchant_id)

        if pagination_params is not None:
            spreadsheets = spreadsheets.order_by(SheetManagement.id.desc()).offset(
                pagination_params.get_skip()).limit(pagination_params.limit)

        return spreadsheets.all()

    @classmethod
    def get_spreadsheet_by_merchant_id(self, merchant_id: str, spreadsheet_id: str, db: Session) -> SheetManagement:
        spreadsheets = db.query(SheetManagement).filter(
            SheetManagement.merchant_id == merchant_id, SheetManagement.spreadsheet_id == spreadsheet_id).first()

        return spreadsheets

    @classmethod
    async def insert_spreadsheet(self, merchant_id: str, spreadsheet_id: str, sheet_type: SheetType, db: Session):
        spreadsheet = SheetManagement(
            merchant_id=merchant_id, spreadsheet_id=spreadsheet_id, sheet_type=sheet_type)

        db.add(spreadsheet)
        db.flush()

        return spreadsheet

    @classmethod
    def count_sheet_own_by_merchant(self, merchant_id: str, db: Session):
        return db.query(func.count()).select_from(SheetManagement).filter(SheetManagement.merchant_id == merchant_id).scalar()
