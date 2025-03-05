from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload, joinedload

from src.buttons.models import ButtonModel
from src.groups.models import GroupModel
from src.groups.schemas import GroupCreateSchema, GroupReadSchema
from src.core.dependencies.db_dependencies import AsyncSessionDI


class GroupRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    # TODO: add limit for groups
    async def create_group(self, project_id: UUID, group: GroupCreateSchema) -> GroupReadSchema:
        group = GroupModel(
            **group.model_dump(),
            project_id=project_id,
        )
        self._session.add(group)
        await self._session.commit()
        await self._session.refresh(group)

        return GroupReadSchema.model_validate(group)

    async def get_groups(self, project_id: UUID) -> list[GroupReadSchema]:
        groups = await self._session.execute(
            select(GroupModel)
            .options(
                selectinload(GroupModel.buttons)
            )
            .where(GroupModel.project_id == project_id)
            .order_by(GroupModel.created_at)
        )
        return [
            GroupReadSchema.model_validate(group)
            for group in groups.scalars().all()
        ]

    async def get_group_by_id(self, group_id: UUID) -> Optional[GroupReadSchema]:
        group = await self._session.execute(
            select(GroupModel)
            .options(
                selectinload(GroupModel.buttons)
            )
            .where(GroupModel.group_id == group_id)
        )
        group = group.scalar()
        if group is None:
            return
        return GroupReadSchema.model_validate(group)

    async def delete_group(self, group_id: UUID):
        await self._session.execute(
            delete(GroupModel)
            .where(GroupModel.group_id == group_id)
        )
        await self._session.commit()
