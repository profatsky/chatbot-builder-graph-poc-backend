from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, delete

from src.buttons.models import ButtonModel
from src.buttons.schemas import ButtonCreateSchema, ButtonReadSchema, ButtonUpdateSchema, ButtonIdWithSeqNumber
from src.core.dependencies.db_dependencies import AsyncSessionDI


class ButtonRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def create_button(self, group_id: UUID, button: ButtonCreateSchema) -> Optional[ButtonReadSchema]:
        button_count = await self._session.scalar(
            select(func.count())
            .select_from(ButtonModel)
            .where(ButtonModel.group_id == group_id)
        )
        button = ButtonModel(
            **button.model_dump(),
            group_id=group_id,
            sequence_number=button_count + 1,
        )
        self._session.add(button)
        await self._session.commit()
        return ButtonReadSchema.model_validate(button)

    async def get_buttons(self, group_id: UUID) -> list[ButtonReadSchema]:
        buttons = await self._session.execute(
            select(ButtonModel)
            .where(ButtonModel.group_id == group_id)
            .order_by(ButtonModel.sequence_number)
        )
        return [
            ButtonReadSchema.model_validate(button)
            for button in buttons.scalars().all()
        ]

    async def get_button_by_id(self, group_id: UUID, button_id: UUID) -> Optional[ButtonReadSchema]:
        button = await self._session.execute(
            select(ButtonModel)
            .where(
                ButtonModel.group_id == group_id,
                ButtonModel.button_id == button_id,
            )
        )
        button = button.scalar()
        if button is None:
            return
        return ButtonReadSchema.model_validate(button)

    async def delete_button(self, group_id: UUID, button_id: UUID):
        await self._session.execute(
            delete(ButtonModel)
            .where(
                ButtonModel.group_id == group_id,
                ButtonModel.button_id == button_id,
            )
        )
        await self._session.commit()

    async def set_button_destination_group(
            self,
            group_id: UUID,
            button_id: UUID,
            destination_group_id: UUID,
    ) -> Optional[ButtonReadSchema]:
        button = await self._session.execute(
            select(ButtonModel)
            .where(
                ButtonModel.group_id == group_id,
                ButtonModel.button_id == button_id,
            )
        )
        button = button.scalar()
        if button is None:
            return

        button.destination_group_id = destination_group_id
        await self._session.commit()

        return ButtonReadSchema.model_validate(button)

    async def update_button(
            self,
            group_id: UUID,
            button_id: UUID,
            button_update: ButtonUpdateSchema,
    ) -> Optional[ButtonReadSchema]:
        button = await self._session.execute(
            select(ButtonModel)
            .where(
                ButtonModel.group_id == group_id,
                ButtonModel.button_id == button_id,
            )
        )
        button = button.scalar()
        if button is None:
            return

        button.text = button_update.text
        button.payload = button_update.payload
        await self._session.commit()

        return ButtonReadSchema.model_validate(button)

    async def change_button_sequence(
            self,
            group_id: UUID,
            button_ids_with_seq_numbers: list[ButtonIdWithSeqNumber],
    ) -> list[ButtonIdWithSeqNumber]:
        id_to_seq_number = {
            btn.button_id: btn.sequence_number
            for btn in button_ids_with_seq_numbers
        }

        buttons = await self._session.execute(
            select(ButtonModel)
            .where(ButtonModel.group_id == group_id)
        )
        buttons = buttons.scalars().all()

        for button in buttons:
            button.sequence_number = id_to_seq_number[button.button_id]
        await self._session.commit()

        return [
            ButtonIdWithSeqNumber.model_validate(button)
            for button in buttons
        ]
