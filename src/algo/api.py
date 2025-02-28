from uuid import UUID

from fastapi import APIRouter, status

from src.algo.dependencies.services_dependencies import AlgoServiceDI
from src.algo.exceptions.http_exceptions import GroupNotFoundHTTPException
from src.algo.exceptions.services_exceptions import GroupNotFoundError
from src.algo.schemas import GroupReadSchema, GroupCreateSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError

router = APIRouter(prefix='/projects/{project_id}', tags=['Algo'])


@router.post(
    '/groups',
    response_model=GroupReadSchema,
)
async def create_group(
        algo_service: AlgoServiceDI,
        project_id: UUID,
        group: GroupCreateSchema,
):
    try:
        return await algo_service.create_group(
            project_id=project_id,
            group=group,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException


@router.get(
    '/groups',
    response_model=list[GroupReadSchema],
)
async def get_groups(
        algo_service: AlgoServiceDI,
        project_id: UUID,
):
    try:
        return await algo_service.get_groups(project_id)
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException


@router.delete(
    '/groups/{group_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
        algo_service: AlgoServiceDI,
        project_id: UUID,
        group_id: UUID,
):
    try:
        await algo_service.delete_group(
            project_id=project_id,
            group_id=group_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
