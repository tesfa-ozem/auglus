# -*- coding: utf-8 -*-
import datetime
from typing import Optional, List, ForwardRef

from pydantic import BaseModel

from app.enums.task import Priority, Status
from app.schemas.professional import ProfessionalBaseSchema

TaskSchema = ForwardRef("TaskSchema")
SkillSchema = ForwardRef("SkillSchema")


class BaseTaskSchema(BaseModel):
    id: int
    name: str
    priority: Priority
    status: Status

    class Config:
        orm_mode = True


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


class UpdateTaskSchema(BaseModel):
    name: Optional[str] = None
    priority: Optional[Priority] = None
    skill: Optional[List[int]] = None
    status: Optional[Status] = None


class GetUserTasksSchema(BaseModel):
    id: int
    start_time: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    task: BaseTaskSchema
    professional: ProfessionalBaseSchema

    class Config:
        orm_mode = True
