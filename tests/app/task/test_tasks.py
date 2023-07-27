import pytest

from core.db import standalone_session
from app.services.task import TaskService


@pytest.mark.asyncio
@standalone_session
async def test_getting_next_task():
    task_service = TaskService()
    result = await task_service.get_next_task()
    assert result
