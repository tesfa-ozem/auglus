from typing import Optional, List, ForwardRef

from pydantic import BaseModel, Field

from app.enums.task import Priority

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

    class Config:
        from_attributes = True
