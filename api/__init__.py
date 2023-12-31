# -*- coding: utf-8 -*-
from fastapi import APIRouter

from api.task.v1.task import task_router
from api.user.v1.user import user_router as user_v1_router
from api.auth.auth import auth_router
from api.skill.v1.skill import skill_router
from api.professional.v1.professional import professional_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(skill_router, prefix="/skill", tags=["Skill"])
router.include_router(
    professional_router, prefix="/professional", tags=["Professional"]
)
router.include_router(task_router, prefix="/task", tags=["Task"])


__all__ = ["router"]
