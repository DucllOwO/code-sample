from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Annotated, Optional
from fastapi import Query
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

import orjson
from pydantic import BaseModel, root_validator
from .constants import PaginationOrder


def orjson_dumps(v: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> float:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.timestamp()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt, float: float}
        allow_population_by_field_name = True
        orm_mode = True
        from_attributes = True

    @root_validator(skip_on_failure=True)
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}


class PaginationParams(ORJSONModel):
    limit: Annotated[int, Query(gt=0, le=100)] = 10  # Per page
    page: Annotated[int, Query(ge=1)] = 1  # Page number
    order: Optional[PaginationOrder] = PaginationOrder.DESC

    def get_skip(self) -> int:
        return (self.page - 1) * self.limit


class PaginationSchema(ORJSONModel):
    page_size: int
    page: int
    total_pages: int
    total_items: int
