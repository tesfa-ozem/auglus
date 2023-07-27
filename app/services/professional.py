from typing import Optional, Sequence, Any, List

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.orm import joinedload

from app.models import Professional, Skill
from core.db import Transactional, session


class ProfessionalService:

    def __int__(self):
        ...

    @Transactional()
    async def create_user(self, first_name: str,
                          last_name: str,
                          user_id: int,
                          skill_ids: List[int]):
        try:
            query = select(Skill).where(Skill.id.in_(skill_ids))
            result = await session.execute(query)
            skill = result.scalars().all()
            professional = Professional(first_name=first_name,
                                        last_name=last_name,
                                        user_id=user_id,
                                        skill=skill)

            session.add(professional)
        except Exception as e:
            raise Exception(f'An unexpected error occurred: {str(e)}')

    async def get_professional_list(self, limit: int = 12,
                                    prev: Optional[int] = None, ) -> List[Professional]:
        query = select(Professional).options(joinedload(Professional.skill))

        if prev:
            query = query.where(Professional.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)

        return result.scalars().unique()

    async def get_available_professionals(self, skill_ids: List[int]) -> List[Professional]:
        query = select(Professional)
        qualified_query = query.join(Professional.skill).filter(Skill.id.in_(skill_ids),).all()
        available_query = qualified_query.filte(Professional.available).all()
        result = await session.execute(available_query)
        return result.scalars().all()

