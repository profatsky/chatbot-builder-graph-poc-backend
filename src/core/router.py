from fastapi import APIRouter

from src.projects.api import router as projects_router
from src.groups.api import router as group_router
from src.buttons.api import router as button_router


def get_app_router() -> APIRouter:
    app_router = APIRouter(prefix='/api')

    routers = [
        projects_router,
        group_router,
        button_router,
    ]

    for router in routers:
        app_router.include_router(router)

    return app_router
