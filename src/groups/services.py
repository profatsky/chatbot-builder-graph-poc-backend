from uuid import UUID

from src.groups.dependencies.repositories_dependencies import GroupRepositoryDI
from src.groups.exceptions.services_exceptions import GroupNotFoundError
from src.groups.schemas import GroupCreateSchema, GroupReadSchema
from src.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.projects.exceptions.services_exceptions import ProjectNotFoundError


class GroupService:
    def __init__(
            self,
            group_repository: GroupRepositoryDI,
            project_repository: ProjectRepositoryDI,
    ):
        self._group_repository = group_repository
        self._project_repository = project_repository

    async def create_group(self, project_id: UUID, group: GroupCreateSchema) -> GroupReadSchema:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        return await self._group_repository.create_group(
            project_id=project_id,
            group=group,
        )

    async def get_groups(self, project_id: UUID) -> list[GroupReadSchema]:
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError
        return await self._group_repository.get_groups(project_id)

    async def delete_group(self, project_id: UUID, group_id: UUID):
        project = await self._project_repository.get_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._group_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        await self._group_repository.delete_group(group_id)
