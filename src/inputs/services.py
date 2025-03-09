from uuid import UUID

from src.groups.dependencies.repositories_dependencies import GroupRepositoryDI
from src.groups.exceptions.services_exceptions import GroupNotFoundError
from src.inputs.dependencies.repositories_dependencies import InputRepositoryDI
from src.inputs.exceptions.services_exceptions import InputNotFoundError, InputTypeConflictError
from src.inputs.schemas import InputReadSchema, InputCreateSchema
from src.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.projects.exceptions.services_exceptions import ProjectNotFoundError


class InputService:
    def __init__(
            self,
            input_repository: InputRepositoryDI,
            project_repository: ProjectRepositoryDI,
            group_repository: GroupRepositoryDI,
    ):
        self._input_repository = input_repository
        self._project_repository = project_repository
        self._group_repository = group_repository

    async def create_input(
            self,
            project_id: UUID,
            group_id: UUID,
            input_field: InputCreateSchema,
    ) -> InputReadSchema:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        input_field = await self._input_repository.create_input(
            group_id=group_id,
            input_field=input_field,
        )
        if input_field is None:
            raise InputTypeConflictError
        return input_field

    async def get_inputs(self, project_id: UUID, group_id: UUID) -> list[InputReadSchema]:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        return await self._input_repository.get_inputs(group_id)

    async def delete_input(self, project_id: UUID, group_id: UUID, input_id: UUID):
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        input_field = await self._input_repository.get_input_by_id(
            group_id=group_id,
            input_id=input_id,
        )
        if input_field is None:
            raise InputNotFoundError

        await self._input_repository.delete_input(
            group_id=group_id,
            input_id=input_id,
        )

    async def set_input_destination_group(
            self,
            project_id: UUID,
            group_id: UUID,
            input_id: UUID,
            destination_group_id: UUID,
    ) -> InputReadSchema:
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

        button = await self._input_repository.get_input_by_id(
            group_id=group_id,
            input_id=input_id,
        )
        if button is None:
            raise InputNotFoundError

        return await self._input_repository.set_input_destination_group(
            group_id=group_id,
            input_id=input_id,
            destination_group_id=destination_group_id,
        )
