# -*- coding: utf-8 -*-
from typing import Optional, List, ForwardRef

from pydantic import BaseModel

from app.enums.task import Priority, Status

TaskSchema = ForwardRef("TaskSchema")
SkillSchema = ForwardRef("SkillSchema")


class SkillSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# class Skill(BaseModel):
#     id: int
#     name: str
#
#     class Config:
#         from_attributes = True


class CreateTaskRequestSchema(BaseModel):
    name: str
    priority: Priority
    skills: Optional[List[int]] = None


class GetTaskResponseSchema(BaseModel):
    id: int
    name: str
    priority: Priority
    skill: Optional[List[SkillSchema]] = None
    status: Status

    class Config:
        from_attributes = True
