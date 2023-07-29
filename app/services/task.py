# -*- coding: utf-8 -*-
import datetime
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, aliased

from app.enums.task import Priority, Status
from app.models import Skill, Task, TaskTracker, Professional
from app.services import UserService
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

        await self.assign_task()

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

    async def get_user_tasks(self, user_id: int, limit: int = 12,
                             prev: Optional[int] = None, ) -> List[TaskTracker]:
        query = select(TaskTracker)
        query = query.join(TaskTracker.professional)
        if not await UserService().is_admin(user_id=user_id):
            query = query.filter(Professional.user_id == user_id)
        query = query.options(
            joinedload(TaskTracker.professional),
            joinedload(TaskTracker.task),

        )

        if prev:
            query = query.where(TaskTracker.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @Transactional()
    async def start_task(self, tracker_id: int):
        if not tracker_id:
            raise Exception("No id provided")
        query = select(TaskTracker).where(TaskTracker.id == tracker_id)
        result = await session.execute(query)
        task_tracker = result.scalars().first()
        task_query = select(Task).join(Task.task_tracker).where(TaskTracker.id == tracker_id)
        task_result = await session.execute(task_query)
        task = task_result.scalars().first()
        if not task_tracker:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.status is not Status.NEW:
            raise HTTPException(status_code=403, detail="Task already started")
        task_tracker.start_time = datetime.datetime.now()
        task.status = Status.IN_PROGRESS

        return task_tracker

    @Transactional()
    async def end_task(self, tracker_id: int):
        if not tracker_id:
            raise Exception("No id provided")
        query = select(TaskTracker).where(TaskTracker.id == tracker_id)
        result = await session.execute(query)
        task_tracker = result.scalars().first()
        task_query = select(Task).join(Task.task_tracker).where(TaskTracker.id == tracker_id)
        task_result = await session.execute(task_query)
        task = task_result.scalars().first()
        if not task_tracker:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.status == Status.COMPLETED:
            raise HTTPException(status_code=403, detail="Task ended")
        task_tracker.end_date = datetime.datetime.now()
        task.status = Status.COMPLETED

        return task_tracker

    @Transactional()
    async def update_task(self, task_id: int, args):
        if not task_id:
            raise Exception("No id provided")
        query = select(Task).options(joinedload(Task.skill)).where(Task.id == task_id)
        result = await session.execute(query)
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Skill not found")

        if args.get('skill', None):
            query = select(Skill).where(Skill.id.in_(args.get('skill')))
            result = await session.execute(query)
            skills_list = result.scalars().all()
            task.skill = skills_list
        del args['skill']

        for key, value in args.items():
            setattr(task, key, value)

        return task

    async def get_next_tasks(self):
        query = select(Task)
        query = (
            query.options(joinedload(Task.skill))
            .order_by(Task.created_at)
            .filter(Task.status == Status.NEW)
        )
        result = await session.execute(query)
        tasks = result.scalars().unique().all()
        tasks_queue = []
        for i in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            for t in tasks:
                if i == t.priority:
                    tasks_queue.append(t)
        return tasks_queue

    @Transactional()
    async def assign_task(self):
        tasks = await self.get_next_tasks()
        professional_service = ProfessionalService()

        for t in tasks:
            skill_ids = [i.id for i in t.skill]
            professionals = (
                await professional_service.get_available_professionals(
                    skill_ids
                )
            )
            processed = await professional_service.process_professionals(
                professionals
            )
            sorted_professionals = sorted(processed, key=lambda x: x[1])
            # Extract the Professional object from the tuple
            # Assign for only professionals with required skills
            for p_tuple in sorted_professionals:
                professional = p_tuple[0]
                # if all(skill in t.skill for skill in professional.skill):
                t.professional = professional
                t.status = Status.ASSIGNED
                professional.available = False
                tracker = TaskTracker(task=t, professional=professional)
                session.add(tracker)
