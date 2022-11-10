from __future__ import annotations

from pydantic import BaseModel, Field


class GetAccessTokenPostRequest(BaseModel):
    apikey: str = Field(..., description="Enter api key", example="9sR16Trz7xD718GyIM8NuaPXj2HEFZY")
    password: str = Field(..., description="Enter password", example="test123!")
    username: str = Field(..., description="Enter username", example="apiuser")


class AccessToken(BaseModel):
    status: bool
    token: str
