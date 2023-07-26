import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.enums.task import Priority, Status
from core.db import Base
from core.db.mixins import TimestampMixin


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    professional: Mapped[List["Professional"]] = relationship("Professional", back_populates="skill")
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped["Task"] = relationship("Task", back_populates="skill")


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    professional: Mapped["Professional"] = relationship("Professional", back_populates="user")


class Professional(Base, TimestampMixin):
    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    available: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="professional")
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    skill: Mapped["Skill"] = relationship("Skill", back_populates="professional")
    task_tracker_id: Mapped[int] = mapped_column(ForeignKey("task_trackers.id"))
    task_tracker: Mapped["TaskTracker"] = relationship("TaskTracker", back_populates="professional")



class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    priority: Mapped[Priority]
    task_tracker_id: Mapped[int] = mapped_column(ForeignKey("task_trackers.id"))
    task_tracker: Mapped["TaskTracker"] = relationship("TaskTracker", back_populates="task")
    skill: Mapped[List["Skill"]] = relationship("Skill", back_populates="task")


class TaskTracker(Base, TimestampMixin):
    __tablename__ = "task_trackers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[Status]
    start_time: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime]
    task: Mapped["Task"] = relationship("Task", back_populates="task_tracker")
    professional: Mapped["Professional"] = relationship("Professional", back_populates="task_tracker")
