from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: bool
    message: Optional[str]
    code: Union[int, List[int]]
    dateTimeBeforeQryExec: datetime


class BaseEntity(BaseModel):
    isActive: Optional[bool]
    isDeleted: Optional[bool]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
