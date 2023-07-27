from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.schemas import ExceptionResponseSchema
from app.schemas.task import CreateTaskRequestSchema, GetTaskResponseSchema
from app.services.skill import SkillService
from app.services.task import TaskService
from core.fastapi.dependencies import PermissionDependency, AllowAll

task_router = APIRouter()


@task_router.post("", dependencies=[Depends(PermissionDependency([AllowAll]))], )
async def create_task(request: CreateTaskRequestSchema):
    task_service = TaskService()
    await task_service.create_task(**request.model_dump())
    return Response(status_code=200)


@task_router.get("", response_model=List[GetTaskResponseSchema],
                 # responses={"400": {"model": ExceptionResponseSchema}},
                 dependencies=[Depends(PermissionDependency([AllowAll]))], )
async def fetch_tasks():
    task_service = TaskService()
    response = await task_service.get_tasks_list()
    return response
