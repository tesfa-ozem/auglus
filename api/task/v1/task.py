# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.schemas.task import CreateTaskRequestSchema, GetTaskResponseSchema, UpdateTaskSchema
from app.services.task import TaskService
from core.fastapi.dependencies import PermissionDependency, AllowAll, IsAuthenticated, IsAdmin

task_router = APIRouter()


@task_router.post(
    "",
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def create_task(request: CreateTaskRequestSchema):
    task_service = TaskService()
    await task_service.create_task(**request.model_dump())
    return Response(status_code=200)


@task_router.get(
    "",
    response_model=List[GetTaskResponseSchema],
    # responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def fetch_tasks():
    task_service = TaskService()
    response = await task_service.get_tasks_list()
    return response


@task_router.patch("/{task_id}", )
async def update_tasks(task_id: int, request: UpdateTaskSchema):
    task_service = TaskService()
    response = await task_service.update_task(task_id=task_id, args=request.model_dump(exclude_unset=True))
    return response
