from typing import Optional

from pydantic import BaseModel, Field

from app.models import User


class CreateProfessionalRequestSchema(BaseModel):
    first_name: str
    last_name: str
    user_id: int
    skill_id: int


class GetProfessionalResponseSchema(BaseModel):
    id: int = Field(description="id")
    first_name: str = Field(description="first_name")
    last_name: str = Field(description="last_name")
    available: bool = Field(description="available")
    user_id: int = Field(description="user")
    skill_id: Optional[int] = None
    task_tracker_id: Optional[int] = None

    class Config:
        orm_mode = True
