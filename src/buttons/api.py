from uuid import UUID

from fastapi import APIRouter, status

from src.buttons.dependencies.services_dependencies import ButtonServiceDI
from src.buttons.exceptions.services_exceptions import ButtonNotFoundError
from src.buttons.schemas import ButtonReadSchema, ButtonCreateSchema
from src.groups.exceptions.http_exceptions import GroupNotFoundHTTPException
from src.groups.exceptions.services_exceptions import GroupNotFoundError
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError

router = APIRouter(
    prefix='/projects/{project_id}/groups/{group_id}/buttons',
    tags=['Buttons'],
)


@router.post(
    '',
    response_model=ButtonReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_button(
        button_service: ButtonServiceDI,
        project_id: UUID,
        group_id: UUID,
        button: ButtonCreateSchema,
):
    try:
        return await button_service.create_button(
            project_id=project_id,
            group_id=group_id,
            button=button,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException


@router.get(
    '',
    response_model=list[ButtonReadSchema],
)
async def get_buttons(
        button_service: ButtonServiceDI,
        project_id: UUID,
        group_id: UUID,
):
    try:
        return await button_service.get_buttons(
            project_id=project_id,
            group_id=group_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException


@router.delete(
    '/{button_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_button(
        button_service: ButtonServiceDI,
        project_id: UUID,
        group_id: UUID,
        button_id: UUID,
):
    try:
        return await button_service.delete_button(
            project_id=project_id,
            group_id=group_id,
            button_id=button_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except ButtonNotFoundError:
        raise ButtonNotFoundError
