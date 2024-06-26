from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    token: str = Field(..., description="Токен")
    old_password: str = Field(..., description='oldPassword', alias="oldPassword")
    new_password: str = Field(..., description='newPassword', alias="newPassword")
