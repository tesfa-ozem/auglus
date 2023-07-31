# -*- coding: utf-8 -*-
import datetime
from typing import Optional, List, Dict

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import Professional, Skill
from core.db import Transactional, session
from collections import defaultdict


class ProfessionalService:
    def __int__(self):
        ...

    @Transactional()
    async def create_user(
            self,
            first_name: str,
            last_name: str,
            user_id: int,
            skill_ids: List[int],
    ):
        try:
            query = select(Skill).where(Skill.id.in_(skill_ids))
            result = await session.execute(query)
            skill = result.scalars().all()
            professional = Professional(
                first_name=first_name,
                last_name=last_name,
                user_id=user_id,
                skill=skill,
            )

            session.add(professional)
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

    async def get_professional_list(
            self,
            limit: int = 12,
            prev: Optional[int] = None,
    ) -> List[Professional]:
        query = select(Professional).options(joinedload(Professional.skill))
        if prev:
            query = query.where(Professional.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)

        return result.scalars().unique()

    async def get_professional_by_id(self, id: int):
        query = select(Professional).where(Professional.id == id)
        return await session.execute(query).scalars().first()

    async def get_available_professionals(
            self, skill: List[int]
    ) -> List[Professional]:
        query = select(Professional)
        query = (
            query.join(Professional.skill)
            .filter(
                Skill.id.in_(skill),
            )
            .order_by(Professional.created_at.asc())
        )
        qualified_query = query.options(
            joinedload(Professional.task_tracker),
            joinedload(Professional.skill),
        ).join(Professional.skill)
        available_query = qualified_query.filter(Professional.available)
        result = await session.execute(available_query)
        return result.scalars().unique().all()

    @Transactional()
    async def update_professional(self, professional_id: int, args):
        if not professional_id:
            raise Exception("No id provided")
        query = select(Professional).options(joinedload(Professional.skill)).where(Professional.id == professional_id)
        result = await session.execute(query)
        professional = result.scalars().first()
        if not professional:
            raise HTTPException(status_code=404, detail="Skill not found")

        if args.get('skill', None):
            query = select(Skill).where(Skill.id.in_(args.get('skill')))
            result = await session.execute(query)
            skills_list = result.scalars().all()
            professional.skill = skills_list
        del args['skill']
        # task.name = args['name']
        for key, value in args.items():
            setattr(professional, key, value)

        return professional

    async def process_professionals(
            self, professionals: List[Professional]
    ) -> List[Dict[Professional, float]]:
        """
        - This function sorts the professionals from oldest to newest
        - It also gets the workload of each professional
        """
        data = []

        if len(professionals) < 1:
            data

        for i in professionals:
            work_load_weight = i.tasks_done / int((
                                                          datetime.datetime.now() - i.created_at).total_seconds()
                                                  )
            data.append((i, work_load_weight))

        return data
