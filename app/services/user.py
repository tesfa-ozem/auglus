# -*- coding: utf-8 -*-
from typing import Optional, List

from sqlalchemy import or_, select, and_

from app.models import User
from app.schemas.user import LoginResponseSchema
from core.db import Transactional, session
from core.exceptions import (
    DuplicateEmailOrUsernameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self):
        ...

    async def get_user_list(
            self,
            limit: int = 12,
            prev: Optional[int] = None,
    ) -> List[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def create_user(
            self, email: str, password: str, user_name: str
    ) -> None:
        # TODO: validate password
        # if password1 != password2:
        #     raise PasswordDoesNotMatchException

        query = select(User).where(
            or_(User.email == email, User.user_name == user_name)
        )
        result = await session.execute(query)
        is_exist = result.scalars().first()
        if is_exist:
            raise DuplicateEmailOrUsernameException

        user = User(email=email, password=password, user_name=user_name)
        session.add(user)
        await session.commit()

        await session.refresh(user)
        user_id = user.id
        await session.close()
        return user_id

    async def is_admin(self, user_id: int) -> bool:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def login(self, email: str, password: str) -> LoginResponseSchema:
        result = await session.execute(
            select(User).where(and_(User.email == email, password == password))
        )
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException

        response = LoginResponseSchema(
            token=TokenHelper.encode(payload={"user_id": user.id, "is_admin": user.is_admin}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response
