from uuid import UUID

from src.actions.dependencies.repositories_dependencies import ActionRepositoryDI
from src.actions.exceptions.services_exceptions import (
    ActionNotFoundError,
    IncorrectNumberOfActionsError,
    ActionIdsMismatchError,
    IncorrectActionSeqNumbersError, IncorrectActionTypeError,
)
from src.actions.schemas import (
    UnionActionCreateSchema,
    UnionActionReadSchema,
    UnionActionUpdateSchema,
    ActionIdWithSeqNumber,
)
from src.actions.utils import get_action_schema_by_type
from src.groups.dependencies.repositories_dependencies import GroupRepositoryDI
from src.groups.exceptions.services_exceptions import GroupNotFoundError
from src.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.projects.exceptions.services_exceptions import ProjectNotFoundError


class ActionService:
    def __init__(
            self,
            action_repository: ActionRepositoryDI,
            project_repository: ProjectRepositoryDI,
            group_repository: GroupRepositoryDI,
    ):
        self._action_repository = action_repository
        self._project_repository = project_repository
        self._group_repository = group_repository

    async def create_action(
            self,
            project_id: UUID,
            group_id: UUID,
            action: UnionActionCreateSchema,
    ) -> UnionActionReadSchema:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        return await self._action_repository.create_action(
            group_id=group_id,
            action=action,
        )

    async def get_actions(self, project_id: UUID, group_id: UUID) -> list[UnionActionReadSchema]:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        return await self._action_repository.get_actions(group_id)

    async def delete_action(self, project_id: UUID, group_id: UUID, action_id: UUID):
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        action = await self._action_repository.get_action_by_id(action_id)
        if action is None:
            raise ActionNotFoundError

        await self._action_repository.delete_action(action_id)

    # TODO: update the sequence numbers of remaining actions after deletion
    async def update_action(
            self,
            project_id: UUID,
            group_id: UUID,
            action_id: UUID,
            action_update: UnionActionUpdateSchema,
    ) -> UnionActionReadSchema:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        action = await self._action_repository.get_action_by_id(action_id)
        if action is None:
            raise ActionNotFoundError

        if not isinstance(action, get_action_schema_by_type(action_update.type)):
            raise IncorrectActionTypeError

        return await self._action_repository.update_action(
            action_id=action_id,
            action_update=action_update,
        )

    async def change_action_sequence(
            self,
            project_id: UUID,
            group_id: UUID,
            action_ids_with_seq_numbers: list[ActionIdWithSeqNumber],
    ) -> list[ActionIdWithSeqNumber]:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        actions = await self._action_repository.get_actions(group_id)
        actions_len = len(actions)
        if actions_len != len(action_ids_with_seq_numbers):
            raise IncorrectNumberOfActionsError

        ids_from_db = []
        ids_from_request = []
        seq_numbers_from_request = []
        for i in range(actions_len):
            ids_from_db.append(actions[i].action_id)
            ids_from_request.append(action_ids_with_seq_numbers[i].action_id)
            seq_numbers_from_request.append(action_ids_with_seq_numbers[i].sequence_number)

        if sorted(ids_from_db) != sorted(ids_from_request):
            raise ActionIdsMismatchError

        if sorted(seq_numbers_from_request) != list(range(1, actions_len + 1)):
            raise IncorrectActionSeqNumbersError

        return await self._action_repository.change_action_sequence(
            group_id=group_id,
            action_ids_with_seq_numbers=action_ids_with_seq_numbers,
        )
