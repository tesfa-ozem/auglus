# -*- coding: utf-8 -*-
from fastapi import APIRouter, Response, Depends

from app.services.analytics import AnalyticsService
from core.fastapi.dependencies import PermissionDependency, IsAuthenticated

home_router = APIRouter()


@home_router.get(
    "/health", dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def home():
    return Response(status_code=200)


@home_router.get("/task-completion-rate")
async def tasks_completion_rate():
    analytics = AnalyticsService()
    result = await analytics.calculate_task_completion_rate()
    return {"task_completion_rate": result}


@home_router.get("/average_task_completion_time")
async def average_task_completion_time():
    analytics = AnalyticsService()
    result = await analytics.calculate_average_task_completion_time()
    return {"average_completion_time": result}


@home_router.get("/workforce_performance")
async def workforce_performance():
    analytics = AnalyticsService()
    result = await analytics.calculate_average_task_completion_time()
    return result
