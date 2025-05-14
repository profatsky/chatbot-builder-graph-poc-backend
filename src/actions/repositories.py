from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectin_polymorphic

from src.actions.models import ActionModel
from src.actions.schemas import (
    UnionActionCreateSchema,
    UnionActionReadSchema,
    UnionActionUpdateSchema,
    ActionIdWithSeqNumber,
)
from src.actions.utils import get_action_model_by_type, validate_action_from_db, UnionActionModel
from src.core.dependencies.db_dependencies import AsyncSessionDI


class ActionRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def create_action(self, group_id: UUID, action: UnionActionCreateSchema) -> UnionActionReadSchema:
        action_count = await self._session.scalar(
            select(func.count())
            .select_from(ActionModel)
            .where(ActionModel.group_id == group_id)
        )
        action_model = get_action_model_by_type(action.type)
        action = action_model(
            **action.model_dump(),
            group_id=group_id,
            sequence_number=action_count + 1,
        )
        self._session.add(action)
        await self._session.commit()
        return validate_action_from_db(action)

    async def get_actions(self, group_id: UUID) -> list[UnionActionReadSchema]:
        actions = await self._get_action_model_instances(group_id)
        return [validate_action_from_db(action) for action in actions]

    async def _get_action_model_instances(self, group_id: UUID) -> list[UnionActionModel]:
        actions = await self._session.execute(
            select(ActionModel)
            .options(
                selectin_polymorphic(ActionModel, ActionModel.__subclasses__()),
            )
            .where(ActionModel.group_id == group_id)
            .order_by(ActionModel.sequence_number)
        )
        return actions.unique().scalars().all()

    async def get_action_by_id(self, action_id: UUID) -> Optional[UnionActionReadSchema]:
        action = await self._get_action_model_instance(action_id)
        if action is None:
            return
        return validate_action_from_db(action)

    async def _get_action_model_instance(self, action_id: UUID) -> Optional[UnionActionModel]:
        action = await self._session.execute(
            select(ActionModel)
            .options(
                selectin_polymorphic(ActionModel, ActionModel.__subclasses__()),
            )
            .where(ActionModel.action_id == action_id)
        )
        if action is None:
            return
        return action.scalar()

    async def update_action(
            self,
            action_id: UUID,
            action_update: UnionActionUpdateSchema,
    ) -> Optional[UnionActionReadSchema]:
        action = await self._get_action_model_instance(action_id)
        if action is None:
            return

        for key, value in action_update.model_dump().items():
            setattr(action, key, value)
        await self._session.commit()

        return validate_action_from_db(action)

    async def delete_action(self, action_id: UUID) -> Optional[UnionActionReadSchema]:
        await self._session.execute(
            delete(ActionModel)
            .where(ActionModel.action_id == action_id)
        )
        await self._session.commit()

    async def change_action_sequence(
            self,
            group_id: UUID,
            action_ids_with_seq_numbers: list[ActionIdWithSeqNumber],
    ) -> list[ActionIdWithSeqNumber]:
        id_to_seq_number = {
            action.action_id: action.sequence_number
            for action in action_ids_with_seq_numbers
        }

        actions = await self._session.execute(
            select(ActionModel)
            .where(ActionModel.group_id == group_id)
        )
        actions = actions.scalars().all()

        for action in actions:
            action.sequence_number = id_to_seq_number[action.action_id]
        await self._session.commit()

        return [
            ActionIdWithSeqNumber.model_validate(action)
            for action in actions
        ]
