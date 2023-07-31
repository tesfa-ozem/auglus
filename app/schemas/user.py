# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


class GetUserListResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    user_name: str = Field(..., description="Username")
    is_admin: bool = Field(..., description="IsAdmin")

    class Config:
        orm_mode = True


class CreateUserRequestSchema(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password1")
    user_name: str = Field(..., description="Username")


class CreateUserResponseSchema(BaseModel):
    email: str = Field(..., description="Email")
    user_name: str = Field(..., description="Username")

    class Config:
        orm_mode = True


class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
    is_admin: str = Field(..., description="IsAdmin")
