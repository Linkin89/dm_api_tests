from __future__ import annotations
from pydantic import BaseModel, Field


class ChangePassword(BaseModel):
    login: str = Field(..., description="Логин")
    token: str = Field(..., description="Токен")
    old_password: str = Field(None, description='oldPassword', serialization_alias="oldPassword")
    new_password: str = Field(None, description='newPassword', serialization_alias="newPassword")
