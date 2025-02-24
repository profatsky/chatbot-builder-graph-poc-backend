from typing import Optional

from sqlalchemy import select, delete

from src.core.dependencies.db_dependencies import AsyncSessionDI
from src.projects.models import ProjectModel
from src.projects.schemas import ProjectCreateSchema, ProjectReadSchema


class ProjectRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def create_project(self, project: ProjectCreateSchema) -> ProjectReadSchema:
        project = ProjectModel(**project.model_dump())
        self._session.add(project)
        await self._session.commit()
        project = await self.get_project(project.project_id)
        return project

    async def get_projects(self) -> list[ProjectReadSchema]:
        projects = await self._session.execute(
            select(ProjectModel)
        )
        projects = projects.unique().scalars().all()
        return [ProjectReadSchema.model_validate(project) for project in projects]

    async def get_project(self, project_id: int) -> Optional[ProjectReadSchema]:
        project = await self._session.execute(
            select(ProjectModel)
            .where(ProjectModel.project_id == project_id)
        )
        project = project.scalar()
        if not project:
            return
        return ProjectReadSchema.model_validate(project)

    async def delete_project(self, project_id: int):
        await self._session.execute(
            delete(ProjectModel)
            .where(
                ProjectModel.project_id == project_id,
            )
        )
        await self._session.commit()