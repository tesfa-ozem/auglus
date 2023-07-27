from typing import Optional, Sequence, Any, List

from sqlalchemy import Row, RowMapping, select

from app.models import Professional
from core.db import Transactional, session


class ProfessionalService:

    def __int__(self):
        ...

    @Transactional()
    async def create_user(self, first_name: str,
                          last_name: str,
                          user_id: int,
                          skill_id: int):
        try:
            professional = Professional(first_name=first_name,
                                        last_name=last_name,
                                        user_id=user_id,
                                        skill_id=skill_id)

            session.add(professional)
        except Exception as e:
            raise Exception(f'An unexpected error occurred: {str(e)}')


    async def get_professional_list(self, limit: int = 12,
                                    prev: Optional[int] = None, ) -> List[Professional]:
        query = select(Professional)

        if prev:
            query = query.where(Professional.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)

        return result.scalars().all()
