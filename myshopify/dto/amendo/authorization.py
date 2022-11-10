from pydantic import BaseModel


class Token(BaseModel):
    status: bool
    token: str
