# -*- coding: utf-8 -*-
from typing import Optional, List

from pydantic import BaseModel, Field


class SkillSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ProfessionalBaseSchema(BaseModel):
    id: int = Field(description="id")
    first_name: str = Field(description="first_name")
    last_name: str = Field(description="last_name")
    available: bool = Field(description="available")
    user_id: int = Field(description="user")

    class Config:
        orm_mode = True


class CreateProfessionalRequestSchema(BaseModel):
    first_name: str
    last_name: str
    user_id: int
    skill_ids: List[int]


class GetProfessionalResponseSchema(BaseModel):
    id: int = Field(description="id")
    first_name: str = Field(description="first_name")
    last_name: str = Field(description="last_name")
    available: bool = Field(description="available")
    user_id: int = Field(description="user")
    skill: Optional[List[SkillSchema]] = None

    class Config:
        orm_mode = True


class UpdateProfessionalSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    available: Optional[bool] = None
    skill: Optional[List[int]] = None
