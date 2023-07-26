from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from core.db import Base
from core.db.mixins import TimestampMixin
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from app.task.enums.task import Priority, Status
import datetime 
from sqlalchemy.orm import relationship
from typing import List

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    priority:Mapped[Priority]
    task_tracker_id: Mapped[int] = mapped_column(ForeignKey("task_trackers.id"))
    task_tracker: Mapped["TaskTracker"] = relationship(back_populates="task")
    skill: Mapped[List["Skill"]] = relationship(back_populates="tasks")



class TaskTracker(Base, TimestampMixin):
    __tablename__ = "task_trackers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[Status]
    start_time: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime]
    task: Mapped["Task"] = relationship(back_populates="task_tracker")
    professional: Mapped["Professional"] = relationship(back_populates="task_tracker")