from typing import Optional, List, Any, Sequence

from sqlalchemy import or_, select, and_, Row, RowMapping

from app.models import Skill
from app.schemas.skill import CreateSkillRequestSchema, GetSkillResponseSchema
from core.db import Transactional, session


class SkillService:

    async def get_skill_list(self, limit: int = 12,
                             prev: Optional[int] = None, ) -> Sequence[Row | RowMapping | Any]:

        query = select(Skill)

        if prev:
            query = query.where(Skill.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def create_list(self, data: CreateSkillRequestSchema):
        skill = Skill(name=data.name)
        session.add(skill)
        return GetSkillResponseSchema(id="1", name=data.name)
