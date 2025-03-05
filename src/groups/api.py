from uuid import UUID

from fastapi import APIRouter, status

from src.groups.dependencies.services_dependencies import GroupServiceDI
from src.groups.exceptions.http_exceptions import GroupNotFoundHTTPException
from src.groups.exceptions.services_exceptions import GroupNotFoundError
from src.groups.schemas import GroupReadSchema, GroupCreateSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError

router = APIRouter(
    prefix='/projects/{project_id}/groups',
    tags=['Groups'],
)


@router.post(
    '',
    response_model=GroupReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
        group_service: GroupServiceDI,
        project_id: UUID,
        group: GroupCreateSchema,
):
    try:
        return await group_service.create_group(
            project_id=project_id,
            group=group,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException


@router.get(
    '',
    response_model=list[GroupReadSchema],
)
async def get_groups(
        group_service: GroupServiceDI,
        project_id: UUID,
):
    try:
        return await group_service.get_groups(project_id)
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException


@router.delete(
    '/{group_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_group(
        group_service: GroupServiceDI,
        project_id: UUID,
        group_id: UUID,
):
    try:
        await group_service.delete_group(
            project_id=project_id,
            group_id=group_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
