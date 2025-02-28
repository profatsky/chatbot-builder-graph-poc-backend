from fastapi import APIRouter

from src.projects.api import router as projects_router
from src.algo.api import router as algo_router


def get_app_router() -> APIRouter:
    app_router = APIRouter(prefix='/api')

    routers = [
        projects_router,
        algo_router,
    ]

    for router in routers:
        app_router.include_router(router)

    return app_router
