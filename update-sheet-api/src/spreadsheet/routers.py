from fastapi import APIRouter, status, Depends
from src.spreadsheet.service import SpreadsheetService
from src.spreadsheet.schemas import SaveSpreadsheetInformationBody, GetSpreadsheetResponse, SpreadsheetWithUrl
from src.database import get_db
from sqlalchemy.orm import Session
from src.exceptions import DetailedHTTPException
from src.spreadsheet.constants import SheetType
from src.utils import build_spreadsheet_url, logging
from src.models import PaginationParams

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('', response_model=GetSpreadsheetResponse)
async def get_spreadsheets_by_merchant_id(merchant_id: str, pagination_params: PaginationParams = Depends(), db: Session = Depends(get_db)):
    try:
        logger.debug(pagination_params)
        total_items_of_merchant = SpreadsheetService.count_sheet_own_by_merchant(
            merchant_id, db)
        spreadsheets = SpreadsheetService.get_spreadsheets_by_merchant_id(
            merchant_id, db, pagination_params)

        result = []
        for temp in spreadsheets:
            temp_result = SpreadsheetWithUrl.model_validate(temp)
            if temp.sheet_type == SheetType.GOOGLE_SHEET:
                temp_result.spreadsheet_url = build_spreadsheet_url(temp.spreadsheet_id)

            result.append(temp_result)

        return {
            'data': result, "pagination": {
                "page_size": len(result),
                "page": pagination_params.page,
                "total_pages": (total_items_of_merchant + pagination_params.limit - 1) // pagination_params.limit,
                "total_items": total_items_of_merchant
            }
        }
    except DetailedHTTPException as client_e:
        raise client_e
    except Exception as e:
        # sentry
        raise e


@router.post('', status_code=status.HTTP_200_OK)
async def save_new_spreadsheet_information(body: SaveSpreadsheetInformationBody, db: Session = Depends(get_db)):
    try:
        logger.debug(body)
        with db.begin():
            new_spreadsheet = await SpreadsheetService.insert_spreadsheet(body.merchant_id, body.spreadsheet_id, body.sheet_type, db)

            return {"id" : new_spreadsheet.id}
    except DetailedHTTPException as client_e:
        raise client_e
    except Exception as e:
        # sentry
        raise e
