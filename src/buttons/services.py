from uuid import UUID

from src.buttons.dependencies.repositories_dependencies import ButtonRepositoryDI
from src.buttons.exceptions.services_exceptions import (
    ButtonNotFoundError,
    ButtonIdsMismatchError,
    IncorrectButtonSeqNumbersError,
    IncorrectNumberOfButtonsError,
)
from src.buttons.schemas import ButtonCreateSchema, ButtonReadSchema, ButtonUpdateSchema, ButtonIdWithSeqNumber
from src.groups.dependencies.repositories_dependencies import GroupRepositoryDI
from src.groups.exceptions.services_exceptions import GroupNotFoundError
from src.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.projects.exceptions.services_exceptions import ProjectNotFoundError


class ButtonService:
    def __init__(
            self,
            button_repository: ButtonRepositoryDI,
            project_repository: ProjectRepositoryDI,
            group_repository: GroupRepositoryDI,
    ):
        self._button_repository = button_repository
        self._project_repository = project_repository
        self._group_repository = group_repository

    async def create_button(
            self,
            project_id: UUID,
            group_id: UUID,
            button: ButtonCreateSchema
    ) -> ButtonReadSchema:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        return await self._button_repository.create_button(
            group_id=group_id,
            button=button,
        )

    async def get_buttons(self, project_id: UUID, group_id: UUID) -> list[ButtonReadSchema]:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        return await self._button_repository.get_buttons(group_id)

    async def delete_button(self, project_id: UUID, group_id: UUID, button_id: UUID):
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        button = await self._button_repository.get_button_by_id(
            group_id=group_id,
            button_id=button_id,
        )
        if button is None:
            raise ButtonNotFoundError

        await self._button_repository.delete_button(
            group_id=group_id,
            button_id=button_id,
        )

    async def set_button_destination_group(
            self,
            project_id: UUID,
            group_id: UUID,
            button_id: UUID,
            destination_group_id: UUID,
    ) -> ButtonReadSchema:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        # TODO: specify group id in errors
        destination_group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=destination_group_id,
        )
        if destination_group is None:
            raise GroupNotFoundError

        button = await self._button_repository.get_button_by_id(
            group_id=group_id,
            button_id=button_id,
        )
        if button is None:
            raise ButtonNotFoundError

        return await self._button_repository.set_button_destination_group(
            group_id=group_id,
            button_id=button_id,
            destination_group_id=destination_group_id,
        )

    async def update_button(
            self,
            project_id: UUID,
            group_id: UUID,
            button_id: UUID,
            button_update: ButtonUpdateSchema,
    ) -> ButtonReadSchema:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        button = await self._button_repository.get_button_by_id(
            group_id=group_id,
            button_id=button_id,
        )
        if button is None:
            raise ButtonNotFoundError

        return await self._button_repository.update_button(
            group_id=group_id,
            button_id=button_id,
            button_update=button_update,
        )

    async def change_button_sequence(
            self,
            project_id: UUID,
            group_id: UUID,
            button_ids_with_seq_numbers: list[ButtonIdWithSeqNumber],
    ) -> list[ButtonIdWithSeqNumber]:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        buttons = await self._button_repository.get_buttons(group_id)
        buttons_len = len(buttons)
        if buttons_len != len(button_ids_with_seq_numbers):
            raise IncorrectNumberOfButtonsError

        ids_from_db = []
        ids_from_request = []
        seq_numbers_from_request = []
        for i in range(buttons_len):
            ids_from_db.append(buttons[i].button_id)
            ids_from_request.append(button_ids_with_seq_numbers[i].button_id)
            seq_numbers_from_request.append(button_ids_with_seq_numbers[i].sequence_number)

        if sorted(ids_from_db) != sorted(ids_from_request):
            raise ButtonIdsMismatchError

        if sorted(seq_numbers_from_request) != list(range(1, buttons_len + 1)):
            raise IncorrectButtonSeqNumbersError

        return await self._button_repository.change_button_sequence(
            group_id=group_id,
            button_ids_with_seq_numbers=button_ids_with_seq_numbers,
        )
