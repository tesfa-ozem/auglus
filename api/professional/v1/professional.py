# -*- coding: utf-8 -*-
from typing import List

from fastapi import APIRouter, Response, Depends
from fastapi.exceptions import HTTPException

from app.schemas import ExceptionResponseSchema
from app.schemas.professional import (
    CreateProfessionalRequestSchema,
    GetProfessionalResponseSchema,
)
from app.services.professional import ProfessionalService
from core.fastapi.dependencies import PermissionDependency, AllowAll

professional_router = APIRouter()


@professional_router.post(
    "",
)
async def create_professional(request: CreateProfessionalRequestSchema):
    professional_service = ProfessionalService()
    await professional_service.create_user(**request.dict())
    return Response(status_code=200)


@professional_router.get(
    "",
    response_model=List[GetProfessionalResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([AllowAll]))],
)
async def fetch_professionals():
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
