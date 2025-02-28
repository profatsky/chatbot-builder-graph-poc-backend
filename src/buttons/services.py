from uuid import UUID

from src.buttons.dependencies.repositories_dependencies import ButtonRepositoryDI
from src.buttons.exceptions.services_exceptions import ButtonNotFoundError
from src.buttons.schemas import ButtonCreateSchema, ButtonReadSchema
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

        group = await self._group_repository.get_group_by_id(group_id)
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

        group = await self._group_repository.get_group_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        return await self._button_repository.get_buttons(group_id)

    async def delete_button(self, project_id: UUID, group_id: UUID, button_id: UUID):
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(group_id)
        if group is None:
            raise GroupNotFoundError

        button = await self._button_repository.get_button_by_id(button_id)
        if button is None:
            raise ButtonNotFoundError

        await self._button_repository.delete_button(button_id)
