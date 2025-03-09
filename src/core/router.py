from fastapi import APIRouter

from src.projects.api import router as projects_router
from src.groups.api import router as groups_router
from src.buttons.api import router as buttons_router
from src.inputs.api import router as inputs_router


def get_app_router() -> APIRouter:
    app_router = APIRouter(prefix='/api')

    routers = [
        projects_router,
        groups_router,
        buttons_router,
        inputs_router,
    ]

    for router in routers:
        app_router.include_router(router)

    return app_router
