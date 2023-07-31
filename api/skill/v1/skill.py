# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Response, Depends

from app.schemas import ExceptionResponseSchema
from app.schemas.skill import CreateSkillRequestSchema, GetSkillResponseSchema, UpdateSkillSchema
from app.services.skill import SkillService
from core.fastapi.dependencies import PermissionDependency, AllowAll
from fastapi import Request

skill_router = APIRouter()


@skill_router.post(
    "",
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def create_skill(request: List[str]):
    skill_service = SkillService()
    await skill_service.create_skill(request)
    return Response(status_code=200)


@skill_router.get(
    "",
    response_model=List[GetSkillResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def fetch_skills(request: Request):
    skill_service = SkillService()
    return await skill_service.get_skill_list()


@skill_router.patch("/{skill_id}")
async def update_skill(skill_id: int, request: Request, args: UpdateSkillSchema):
    skill_service = SkillService()
    return await skill_service.update_skills(skill_id=skill_id, args=request.dict())
