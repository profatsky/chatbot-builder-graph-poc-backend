from uuid import UUID

from src.algo.dependencies.repositories_dependencies import AlgoRepositoryDI
from src.algo.exceptions.services_exceptions import GroupNotFoundError
from src.algo.schemas import GroupCreateSchema, GroupReadSchema
from src.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.projects.exceptions.services_exceptions import ProjectNotFoundError


class AlgoService:
    def __init__(
            self,
            algo_repository: AlgoRepositoryDI,
            project_repository: ProjectRepositoryDI,
    ):
        self._algo_repository = algo_repository
        self._project_repository = project_repository

    async def create_group(self, project_id: UUID, group: GroupCreateSchema) -> GroupReadSchema:
        project = await self._project_repository.get_project(project_id)
        if project is None:
            raise ProjectNotFoundError

        return await self._algo_repository.create_group(
            project_id=project_id,
            group=group,
        )

    async def get_groups(self, project_id: UUID) -> list[GroupReadSchema]:
        project = await self._project_repository.get_project(project_id)
        if project is None:
            raise ProjectNotFoundError
        return await self._algo_repository.get_groups(project_id)

    async def delete_group(self, project_id: UUID, group_id: UUID):
        project = await self._project_repository.get_project(project_id)
        if project is None:
            raise ProjectNotFoundError

        group = await self._algo_repository.get_group_by_id(
            project_id=project_id,
            group_id=group_id,
        )
        if group is None:
            raise GroupNotFoundError

        await self._algo_repository.delete_group(
            project_id=project_id,
            group_id=group_id,
        )
