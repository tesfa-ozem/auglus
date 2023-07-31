# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.schemas.task import CreateTaskRequestSchema, GetTaskResponseSchema, UpdateTaskSchema, GetUserTasksSchema
from app.services.task import TaskService
from core.fastapi.dependencies import PermissionDependency, AllowAll, IsAuthenticated, IsAdmin
from fastapi import Request

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
    "/all",
    response_model=List[GetTaskResponseSchema],
    # responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def fetch_tasks(request: Request):
    task_service = TaskService()
    response = await task_service.get_tasks_list()
    return response


@task_router.patch("/{task_id}", dependencies=[Depends(PermissionDependency([IsAdmin]))])
async def update_tasks(task_id: int, request: UpdateTaskSchema):
    task_service = TaskService()
    response = await task_service.update_task(task_id=task_id, args=request.model_dump(exclude_unset=True))
    return response


@task_router.patch("/{tracker_id}/start", dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
async def start_tasks(tracker_id: int, ):
    task_service = TaskService()
    response = await task_service.start_task(tracker_id)
    return response


@task_router.patch("/{tracker_id}/end", dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
async def end_tasks(tracker_id: int, ):
    task_service = TaskService()
    response = await task_service.end_task(tracker_id)
    return response


@task_router.get('/userTasks', response_model=List[GetUserTasksSchema],
                 dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
async def fetch_user_tasks(request: Request):
    task_service = TaskService()
    response = await task_service.get_user_tasks(user_id=request.user.id)
    return response


@task_router.post('/assign_task', dependencies=[Depends(PermissionDependency([IsAdmin]))])
async def assign_task():
    task_service = TaskService()
    await task_service.assign_task()
    return Response(status_code=200, content='Assigning task')
