from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from core.db import Base
from core.db.mixins import TimestampMixin
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship


class Professional(Base, TimestampMixin):
    __tablename__ = "professionals"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name:Mapped[str]
    last_name:Mapped[str]
    available:Mapped[bool]
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    skill: Mapped["Skill"] = relationship(back_populates="professionals")
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    parent: Mapped["User"] = relationship(back_populates="professionals")
    task_tracker_id: Mapped[int] = mapped_column(ForeignKey("task_trackers.id"))
    task_tracker: Mapped["TaskTracker"] = relationship(back_populates="professionals")

