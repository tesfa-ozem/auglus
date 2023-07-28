# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


class CreateSkillRequestSchema(BaseModel):
    name: str


class GetSkillResponseSchema(BaseModel):
    id: int = Field(..., description="id")
    name: str = Field(..., description="name")

    class Config:
        orm_mode = True


class UpdateSkillSchema(CreateSkillRequestSchema):
    ...
