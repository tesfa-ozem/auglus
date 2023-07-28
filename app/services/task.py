# -*- coding: utf-8 -*-
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.enums.task import Priority, Status
from app.models import Skill, Task, TaskTracker
from app.services.professional import ProfessionalService
from core.db import Transactional, session


class TaskService:
    @Transactional()
    async def create_task(
            self, name: str, priority: Priority, skills: Optional[List[int]] = None
    ):
        if len(skills) > 0:
            query = select(Skill).where(Skill.id.in_(skills))
            result = await session.execute(query)
            skills_list = result.scalars().all()
        task = Task(name=name, priority=priority, skill=skills_list)
        # skill = task(name=data.name)
        session.add(task)

        await self.assign_task(skills)

    async def get_tasks_list(
            self,
            limit: int = 12,
            prev: Optional[int] = None,
    ) -> List[Task]:
        query = select(Task).options(joinedload(Task.skill))
        if prev:
            query = query.where(Task.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().unique()

    async def get_next_task(self, limit):
        query = select(Task)
        query = query.order_by(Task.priority.desc(), Task.created_at).filter(Task.status == Status.NEW)
        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def assign_task(self, skills: List[int]):
        professional_service = ProfessionalService()
        professionals = await professional_service.get_available_professionals(skills)
        processed = await professional_service.process_professionals(professionals)
        tasks = await self.get_next_task(limit=len(processed))
        # sorted_professionals = sorted(processed)
        sorted_professionals = sorted(processed, key=lambda x: x[1])
        for t, p in zip(tasks, sorted_professionals):
            t.professional = p
            t.status = Status.IN_PROGRESS
            p[0].available = False
            tracker = TaskTracker(task=t, professional=p[0])
            session.add(tracker)
