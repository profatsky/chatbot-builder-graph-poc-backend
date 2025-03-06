from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Body

from src.buttons.dependencies.services_dependencies import ButtonServiceDI
from src.buttons.exceptions.http_exceptions import (
    ButtonNotFoundHTTPException,
    ButtonIdsMismatchHTTPException,
    IncorrectButtonSeqNumbersHTTPException,
    IncorrectNumberOfButtonsHTTPException,
)
from src.buttons.exceptions.services_exceptions import (
    ButtonNotFoundError,
    ButtonIdsMismatchError,
    IncorrectButtonSeqNumbersError,
    IncorrectNumberOfButtonsError,
)
from src.buttons.schemas import ButtonReadSchema, ButtonCreateSchema, ButtonUpdateSchema, ButtonIdWithSeqNumber
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


@router.patch(
    '/{button_id}/destination',
    response_model=ButtonReadSchema,
)
async def set_button_destination_group(
        button_service: ButtonServiceDI,
        project_id: UUID,
        group_id: UUID,
        button_id: UUID,
        destination_group_id: Annotated[UUID, Body(embed=True)],
):
    try:
        return await button_service.set_button_destination_group(
            project_id=project_id,
            group_id=group_id,
            button_id=button_id,
            destination_group_id=destination_group_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except ButtonNotFoundError:
        raise ButtonNotFoundHTTPException


@router.put(
    '/{button_id}',
    response_model=ButtonReadSchema,
)
async def update_button(
        button_service: ButtonServiceDI,
        project_id: UUID,
        group_id: UUID,
        button_id: UUID,
        button_update: ButtonUpdateSchema,
):
    try:
        return await button_service.update_button(
            project_id=project_id,
            group_id=group_id,
            button_id=button_id,
            button_update=button_update,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except ButtonNotFoundError:
        raise ButtonNotFoundHTTPException


@router.post(
    '/sequence',
    response_model=list[ButtonIdWithSeqNumber],
)
async def change_button_sequence(
        button_service: ButtonServiceDI,
        project_id: UUID,
        group_id: UUID,
        button_ids_with_seq_numbers: list[ButtonIdWithSeqNumber],
):
    try:
        return await button_service.change_button_sequence(
            project_id=project_id,
            group_id=group_id,
            button_ids_with_seq_numbers=button_ids_with_seq_numbers,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except IncorrectNumberOfButtonsError:
        raise IncorrectNumberOfButtonsHTTPException
    except ButtonIdsMismatchError:
        raise ButtonIdsMismatchHTTPException
    except IncorrectButtonSeqNumbersError:
        raise IncorrectButtonSeqNumbersHTTPException
