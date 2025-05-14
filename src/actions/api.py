from uuid import UUID

from fastapi import APIRouter, status

from src.actions.dependencies.services_dependencies import ActionServiceDI
from src.actions.exceptions.http_exceptions import (
    ActionNotFoundHTTPException,
    IncorrectNumberOfActionsHTTPException,
    ActionIdsMismatchHTTPException,
    IncorrectActionSeqNumbersHTTPException, IncorrectActionTypeHTTPException,
)
from src.actions.exceptions.services_exceptions import (
    ActionNotFoundError,
    IncorrectNumberOfActionsError,
    ActionIdsMismatchError,
    IncorrectActionSeqNumbersError, IncorrectActionTypeError,
)
from src.actions.schemas import (
    UnionActionReadSchema,
    UnionActionCreateSchema,
    UnionActionUpdateSchema,
    ActionIdWithSeqNumber,
)
from src.groups.exceptions.http_exceptions import GroupNotFoundHTTPException
from src.groups.exceptions.services_exceptions import GroupNotFoundError
from src.projects.exceptions.http_exceptions import ProjectNotFoundHTTPException
from src.projects.exceptions.services_exceptions import ProjectNotFoundError

router = APIRouter(
    prefix='/projects/{project_id}/groups/{group_id}/actions',
    tags=['Actions'],
)


@router.post(
    '',
    response_model=UnionActionReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_action(
        actions_service: ActionServiceDI,
        project_id: UUID,
        group_id: UUID,
        action: UnionActionCreateSchema,
):
    try:
        return await actions_service.create_action(
            project_id=project_id,
            group_id=group_id,
            action=action,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException


@router.get(
    '',
    response_model=list[UnionActionReadSchema],
)
async def get_actions(
        action_service: ActionServiceDI,
        project_id: UUID,
        group_id: UUID,
):
    try:
        return await action_service.get_actions(
            project_id=project_id,
            group_id=group_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException


@router.delete(
    '/{action_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_action(
        action_service: ActionServiceDI,
        project_id: UUID,
        group_id: UUID,
        action_id: UUID,
):
    try:
        return await action_service.delete_action(
            project_id=project_id,
            group_id=group_id,
            action_id=action_id,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except ActionNotFoundError:
        raise ActionNotFoundHTTPException


@router.put(
    '/{action_id}',
    response_model=UnionActionReadSchema,
)
async def update_action(
        action_service: ActionServiceDI,
        project_id: UUID,
        group_id: UUID,
        action_id: UUID,
        action_update: UnionActionUpdateSchema,
):
    try:
        return await action_service.update_action(
            project_id=project_id,
            group_id=group_id,
            action_id=action_id,
            action_update=action_update,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except ActionNotFoundError:
        raise ActionNotFoundHTTPException
    except IncorrectActionTypeError:
        raise IncorrectActionTypeHTTPException


@router.post(
    '/sequence',
    response_model=list[ActionIdWithSeqNumber],
)
async def change_action_sequence(
        action_service: ActionServiceDI,
        project_id: UUID,
        group_id: UUID,
        action_ids_with_seq_numbers: list[ActionIdWithSeqNumber],
):
    try:
        return await action_service.change_action_sequence(
            project_id=project_id,
            group_id=group_id,
            action_ids_with_seq_numbers=action_ids_with_seq_numbers,
        )
    except ProjectNotFoundError:
        raise ProjectNotFoundHTTPException
    except GroupNotFoundError:
        raise GroupNotFoundHTTPException
    except IncorrectNumberOfActionsError:
        raise IncorrectNumberOfActionsHTTPException
    except ActionIdsMismatchError:
        raise ActionIdsMismatchHTTPException
    except IncorrectActionSeqNumbersError:
        raise IncorrectActionSeqNumbersHTTPException
