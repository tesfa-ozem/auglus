# -*- coding: utf-8 -*-
from typing import Optional, Any, Sequence

from fastapi import HTTPException
from sqlalchemy import select, Row, RowMapping

from app.models import Skill
from app.schemas.skill import CreateSkillRequestSchema, GetSkillResponseSchema
from core.db import Transactional, session


class SkillService:
    async def get_skill_list(
            self,
            limit: int = 12,
            prev: Optional[int] = None,
    ) -> Sequence[Row | RowMapping | Any]:
        query = select(Skill)

        if prev:
            query = query.where(Skill.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def create_skill(self, data: CreateSkillRequestSchema):
        skill = Skill(name=data.name)
        session.add(skill)
        return GetSkillResponseSchema(id="1", name=data.name)

    @Transactional()
    async def update_skills(self, skill_id: int, args):
        if not skill_id:
            raise Exception("No id provided")

        query = select(Skill).where(Skill.id == skill_id)
        result = await session.execute(query)
        skill = result.scalars().first()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")
        skill.name = args['name']

        return skill
