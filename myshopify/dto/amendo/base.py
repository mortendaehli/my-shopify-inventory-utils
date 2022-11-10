from datetime import datetime

from pydantic import BaseModel


class ResponseBase(BaseModel):
    status: bool
    message: str
    code: int
    dateTimeBeforeQryExec: datetime
