from sqlalchemy import Column, Unicode, BigInteger, Boolean

from core.db import Base
from core.db.mixins import TimestampMixin
from typing import List
from app.professional.models import Professional
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    professional: Mapped[List["Professional"]] = relationship(back_populates="skills")
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped["Task"] = relationship(back_populates="skills")
