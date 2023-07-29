# -*- coding: utf-8 -*-
from fastapi import APIRouter, Response, Depends

from core.fastapi.dependencies import PermissionDependency, AllowAll, IsAuthenticated

home_router = APIRouter()


@home_router.get(
    "/health", dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def home():
    return Response(status_code=200)
