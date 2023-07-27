import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, Table, Column, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.enums.task import Priority, Status
from core.db import Base
from core.db.mixins import TimestampMixin

task_skills_table = Table(
    "task_skills",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)

professional_skills_table = Table(
    "professional_skills",
    Base.metadata,
    Column("professional_id", Integer, ForeignKey("professionals.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)


class Skill(Base, TimestampMixin):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    professional: Mapped[Optional[List["Professional"]]] = relationship("Professional",
                                                                         secondary=professional_skills_table,
                                                                         back_populates="skill")
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"))
    task: Mapped[Optional["Task"]] = relationship("Task", secondary=task_skills_table, back_populates="skill")


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    professional: Mapped[Optional["Professional"]] = relationship("Professional", back_populates="user")


class Professional(Base, TimestampMixin):
    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    available: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="professional")
    skill: Mapped[Optional[List["Skill"]]] = relationship("Skill", secondary=professional_skills_table,
                                                    back_populates="professional")
    task_tracker_id: Mapped[Optional[int]] = mapped_column(ForeignKey("task_trackers.id"))
    task_tracker: Mapped[Optional[List["TaskTracker"]]] = relationship("TaskTracker", back_populates="professional")


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    priority: Mapped[Priority]
    task_tracker_id: Mapped[Optional[int]] = mapped_column(ForeignKey("task_trackers.id"))
    task_tracker: Mapped[Optional["TaskTracker"]] = relationship("TaskTracker", back_populates="task")
    skill: Mapped[Optional[List["Skill"]]] = relationship("Skill", secondary=task_skills_table, back_populates="task")
    status: Mapped[Status] = mapped_column(default=Status.NEW)


class TaskTracker(Base, TimestampMixin):
    __tablename__ = "task_trackers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_time: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime]
    task: Mapped["Task"] = relationship("Task", back_populates="task_tracker")
    professional: Mapped["Professional"] = relationship("Professional", back_populates="task_tracker")
