# -*- coding: utf-8 -*-
import pytest

from app.services.professional import ProfessionalService
from core.db import standalone_session
from app.services.task import TaskService


@pytest.mark.asyncio
@standalone_session
async def test_getting_next_task():
    task_service = TaskService()
    result = await task_service.get_next_task(limit=12)
    assert result


@pytest.mark.asyncio
@standalone_session
async def test_getting_available_professionals():
    professional_service = ProfessionalService()
    result = await professional_service.get_available_professionals(skill_ids=[1, 2])
    assert result

@pytest.mark.asyncio
@standalone_session
async def test_assign_task():
    task_service = TaskService()
    await task_service.assign_task([2])
