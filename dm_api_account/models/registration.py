from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    email: str = Field(..., description="E-mail")