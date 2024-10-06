from sqlalchemy import Column, String, TIMESTAMP, func, Integer, Enum
from ..database import Base
from src.spreadsheet.constants import SheetType


class SheetManagement(Base):
    __tablename__ = "sheet_management"

    id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(String, nullable=False)
    # id get from the google sheet link or auto generated id for microsoft excel
    spreadsheet_id = Column(String, nullable=False)
    # MICROSOFT_EXCEL OR GOOGLE_SHEET
    sheet_type = Column(Enum(SheetType), nullable=False)
    # app_script_id = Column(String, nullable=False)  # to call app script
    created_at = Column(TIMESTAMP, server_default=func.now())
