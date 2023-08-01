# -*- coding: utf-8 -*-
from typing import Dict

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app.enums.task import Status
from app.models import Task, TaskTracker
from core.db import Base, session


class AnalyticsService:
    async def get_table_row_count(self, model: Base, condition=None):
        query = select(func.count()).select_from(model)
        if condition is not None:
            query = query.filter(condition)
        result = await session.execute(query)
        row_count = result.scalar_one()
        return row_count

    async def calculate_task_completion_rate(self):
        """
        Calculates total tasks completed against task available
        """
        total_tasks = await self.get_table_row_count(Task)
        completed_tasks = await self.get_table_row_count(
            Task, Task.status == Status.COMPLETED
        )
        if total_tasks == 0:
            return 0.0
        return (completed_tasks / total_tasks) * 100

    async def calculate_average_task_completion_time(
        self,
    ):
        """
        Calculates how long a task takes to complete on average.
        Time returned is in seconds
        """
        completed_tasks_count = await self.get_table_row_count(
            Task, Task.status == Status.COMPLETED
        )
        query = select(TaskTracker)
        query = query.join(TaskTracker.task)
        query = query.where(Task.status == Status.COMPLETED)
        result = await session.execute(query)
        completed_tasks = result.scalars().all()
        total_duration = sum(
            (task.end_date - task.start_time).total_seconds()
            for task in completed_tasks
        )

        if completed_tasks_count == 0:
            return 0.0
        return total_duration / completed_tasks_count

    async def calculate_workforce_performance(self):
        """
        Calculates the task completion rate and tasks completed
        per professional
        """
        workforce_performance: Dict[str, Dict[str, float]] = {}
        query = select(TaskTracker)
        query = query.options(
            joinedload(TaskTracker.professional), joinedload(TaskTracker.task)
        )

        result = await session.execute(query)
        task_tracker = result.scalars().unique().all()
        professionals = set(task.professional for task in task_tracker)
        for professional in professionals:
            if professional is None:
                continue
            professional_tasks = [
                task
                for task in task_tracker
                if task.professional == professional
            ]
            total_duration = sum(
                (task.end_date - task.start_time).total_seconds()
                for task in professional_tasks
                if task.task is not None
                and task.task.status == Status.COMPLETED
            )
            total_completed_tasks = sum(
                1
                for task in professional_tasks
                if task.task is not None
                and task.task.status == Status.COMPLETED
            )
            if total_completed_tasks == 0:
                average_completion_time = 0.0
            else:
                average_completion_time = total_duration / total_completed_tasks
            workforce_performance[professional.first_name] = {
                "completed_tasks": total_completed_tasks,
                "average_completion_time": average_completion_time,
            }
        return workforce_performance
