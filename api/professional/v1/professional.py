# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Response, Depends
from fastapi.exceptions import HTTPException

from app.schemas import ExceptionResponseSchema
from app.schemas.professional import (
    CreateProfessionalRequestSchema,
    GetProfessionalResponseSchema,
    UpdateProfessionalSchema,
)
from app.services.professional import ProfessionalService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated,
)
from fastapi import Request

professional_router = APIRouter()


@professional_router.post(
    "",
)
async def create_professional(
    request: Request, args: CreateProfessionalRequestSchema
):
    professional_service = ProfessionalService()
    await professional_service.create_user(**args.dict())
    return Response(status_code=200)


@professional_router.get(
    "",
    response_model=List[GetProfessionalResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def fetch_professionals(request: Request):
    try:
        professional_service = ProfessionalService()
        response = await professional_service.get_professional_list()
        # breakpoint()
        return response
    except Exception as e:
        # Catch and handle the validation error
        # You can return a custom error response
        error_msg = "Validation error: " + str(e)
        raise HTTPException(status_code=422, detail=error_msg)


@professional_router.get(
    "/{professional_id}",
    response_model=GetProfessionalResponseSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def fetch_professional_by_id(professional_id: int):
    professional_service = ProfessionalService()
    response = await professional_service.get_professional_by_id(
        professional_id
    )
    return response


@professional_router.patch(
    "/{professional_id}",
)
async def update_professionals(
    professional_id: int, request: Request, args: UpdateProfessionalSchema
):
    professional_service = ProfessionalService()
    response = await professional_service.update_professional(
        professional_id, args.model_dump(exclude_unset=True)
    )
    return response
