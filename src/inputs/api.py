from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, Body

from src.groups.exceptions.http_exceptions import GroupNotFoundHTTPException
from src.groups.exceptions.services_exceptions import GroupNotFoundError
from src.inputs.dependencies.services_dependencies import InputServiceDI
from src.inputs.exceptions.http_exceptions import InputNotFoundHTTPException, InputTypeConflictHTTPException
from src.inputs.exceptions.services_exceptions import InputNotFoundError, InputTypeConflictError
from src.inputs.schemas import InputReadSchema, InputCreateSchema
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError


# TODO: add endpoint for update input
router = APIRouter(
    prefix='/projects/{project_id}/groups/{group_id}/inputs',
    tags=['Inputs'],
)


@router.post(
    '',
    response_model=InputReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_input(
        input_service: InputServiceDI,
        project_id: UUID,
        group_id: UUID,
        input_field: InputCreateSchema,
):
    try:
        return await input_service.create_input(
            project_id=project_id,
            group_id=group_id,
            input_field=input_field,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except InputTypeConflictError:
        raise InputTypeConflictHTTPException


@router.get(
    '',
    response_model=list[InputReadSchema],
)
async def get_inputs(
        input_service: InputServiceDI,
        project_id: UUID,
        group_id: UUID,
):
    try:
        return await input_service.get_inputs(
            project_id=project_id,
            group_id=group_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException


@router.delete(
    '/{input_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_input(
        input_service: InputServiceDI,
        project_id: UUID,
        group_id: UUID,
        input_id: UUID,
):
    try:
        return await input_service.delete_input(
            project_id=project_id,
            group_id=group_id,
            input_id=input_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except InputNotFoundError:
        raise InputNotFoundHTTPException


@router.patch(
    '/{input_id}/destination',
    response_model=InputReadSchema,
)
async def set_input_destination_group(
        input_service: InputServiceDI,
        project_id: UUID,
        group_id: UUID,
        input_id: UUID,
        destination_group_id: Annotated[UUID, Body(embed=True)],
):
    try:
        return await input_service.set_input_destination_group(
            project_id=project_id,
            group_id=group_id,
            input_id=input_id,
            destination_group_id=destination_group_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except InputNotFoundError:
        raise InputNotFoundHTTPException
