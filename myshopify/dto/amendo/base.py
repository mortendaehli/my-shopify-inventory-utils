from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: bool
    message: Optional[str]
    code: Union[int, List[int]]
    dateTimeBeforeQryExec: Optional[
        str
    ]  # Fixme: This should be YYYY-MM-DD HH:MM:SS, but somehow it is Norwegian format...


class BaseEntity(BaseModel):
    isActive: Optional[bool]
    isDeleted: Optional[bool]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
