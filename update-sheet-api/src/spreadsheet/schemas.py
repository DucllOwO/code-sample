from src.models import ORJSONModel, PaginationSchema
from src.spreadsheet.constants import SheetType
from uuid import uuid4
from pydantic import model_validator, BaseModel
from typing import Optional
from src.utils import logging, get_spreadsheet_id

logger = logging.getLogger(__name__)


class SaveSpreadsheetInformationBody(BaseModel):
    merchant_id: str
    spreadsheet_url: Optional[str] = None
    spreadsheet_id: Optional[str] = None
    sheet_type: SheetType

    @model_validator(mode='after')
    def validate_spreadsheet_url(cls, values):
        sheet_type = values.sheet_type
        spreadsheet_url = values.spreadsheet_url

        if sheet_type == SheetType.MICROSOFT_EXCEL:
            # Generate UUID if not provided for MICROSOFT_EXCEL
            values.spreadsheet_id = str(uuid4())
            return values
        elif sheet_type == SheetType.GOOGLE_SHEET and spreadsheet_url is None:
            raise ValueError("spreadsheet_url is required for GOOGLE_SHEET")

        values.spreadsheet_id = get_spreadsheet_id(spreadsheet_url)
        logger.debug(get_spreadsheet_id(spreadsheet_url))

        if values.spreadsheet_id is None:
            raise ValueError("spreadsheet_url format is incorrect")

        return values


class Spreadsheet(ORJSONModel):
    id: int
    merchant_id: str
    spreadsheet_id: str
    sheet_type: SheetType


class SpreadsheetWithUrl(ORJSONModel):
    # This class different with Spreadsheet is that it has field "spreadsheet_url" instead of "spreadsheet_id"
    id: int
    merchant_id: str
    # if the sheet_type is 'MICROSOFT_EXCEL' this field is null
    spreadsheet_url: Optional[str] = None
    sheet_type: SheetType


class GetSpreadsheetResponse(ORJSONModel):
    data: list[SpreadsheetWithUrl]
    pagination: PaginationSchema
