from fastapi import APIRouter, status

from src.projects.dependencies.services_dependencies import ProjectServiceDI
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError
from src.projects.schemas import ProjectReadSchema, ProjectCreateSchema

router = APIRouter(prefix='/projects', tags=['Projects'])


@router.post(
    '',
    response_model=ProjectReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
        project_service: ProjectServiceDI,
        project: ProjectCreateSchema,
):
    return await project_service.create_project(project)


@router.get(
    '',
    response_model=list[ProjectReadSchema],
)
async def get_projects(
        project_service: ProjectServiceDI,
):
    return await project_service.get_projects()


@router.delete(
    '/{project_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
        project_service: ProjectServiceDI,
        project_id: int,
):
    try:
        await project_service.delete_project(project_id)
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
