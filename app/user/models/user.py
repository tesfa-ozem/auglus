from sqlalchemy import Column, Unicode, BigInteger, Boolean

from core.db import Base
from core.db.mixins import TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped



class User(Base, TimestampMixin):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(nullable=False, unique=True)
    user_name:Mapped[str] = mapped_column(nullable=False, unique=True)
    is_admin:Mapped[bool] = mapped_column(default=False)
    child: Mapped["Professional"] = relationship(back_populates="user")
