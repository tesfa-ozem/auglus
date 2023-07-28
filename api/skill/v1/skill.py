# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Response, Depends

from app.schemas import ExceptionResponseSchema
from app.schemas.skill import CreateSkillRequestSchema, GetSkillResponseSchema
from app.services.skill import SkillService
from core.fastapi.dependencies import PermissionDependency, AllowAll

skill_router = APIRouter()


@skill_router.post(
    "",
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def create_skill(request: CreateSkillRequestSchema):
    skill_service = SkillService()
    await skill_service.create_skill(request)
    return Response(status_code=200)


@skill_router.get(
    "",
    response_model=List[GetSkillResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def fetch_skills():
    skill_service = SkillService()
    return await skill_service.get_skill_list()
