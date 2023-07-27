from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.enums.task import Priority
from app.models import Skill, Task
from core.db import Transactional, session


class TaskService:
    @Transactional()
    async def create_task(self, name: str,
                          priority: Priority,
                          skills: Optional[List[int]] = None):
        if len(skills) > 0:
            query = select(Skill).where(Skill.id.in_(skills))
            result = await session.execute(query)
            skills_list = result.scalars().all()
        task = Task(name=name, priority=priority, skill=skills_list)
        # skill = task(name=data.name)
        session.add(task)

    async def get_tasks_list(self, limit: int = 12,
                             prev: Optional[int] = None, ) -> List[Task]:
        query = select(Task).options(joinedload(Task.skill))
        if prev:
            query = query.where(Task.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().unique()

    async def get_next_task(self):
        query = select(Task)
        query = query.order_by(Task.priority.desc(), Task.created_at)
        result = await session.execute(query)
        return result.scalars().first()
