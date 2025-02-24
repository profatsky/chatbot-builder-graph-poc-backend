from src.projects.dependencies.repositories_dependencies import ProjectRepositoryDI
from src.projects.exceptions.services_exceptions import ProjectNotFoundError
from src.projects.schemas import ProjectCreateSchema, ProjectReadSchema


class ProjectService:
    def __init__(self, project_repository: ProjectRepositoryDI):
        self._project_repository = project_repository

    async def create_project(self, project: ProjectCreateSchema) -> ProjectReadSchema:
        return await self._project_repository.create_project(project)

    async def get_projects(self) -> list[ProjectReadSchema]:
        return await self._project_repository.get_projects()

    async def delete_project(self, project_id: int):
        project = self._project_repository.get_project(project_id)
        if project is None:
            raise ProjectNotFoundError

        await self._project_repository.delete_project(project_id)