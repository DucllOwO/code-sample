from sqlalchemy import Column, String, TIMESTAMP, func, text, Integer, Enum
from ..database import Base
from .constants import CallbackStatus


class CallbackHistory(Base):
    __tablename__ = "callback_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(String, nullable=False) 
    # to find the right sheet in app scripts
    spreadsheet_id = Column(String, nullable=False)
    sheet_id = Column(String, nullable=False)
    app_id = Column(String, nullable=False)  # to call app script
    order_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(Enum(CallbackStatus), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
