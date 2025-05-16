from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from src.core.dependencies.db_dependencies import AsyncSessionDI
from src.inputs.models import InputModel
from src.inputs.schemas import InputCreateSchema, InputReadSchema


class InputRepository:
    def __init__(self, session: AsyncSessionDI):
        self._session = session

    async def _get_input_model_instance(self, input_id: UUID) -> Optional[InputModel]:
        input_field = await self._session.execute(
            select(InputModel)
            .where(InputModel.input_id == input_id)
        )
        input_field = input_field.scalar()
        if input_field is None:
            return
        return input_field

    async def create_input(self, group_id: UUID, input_field: InputCreateSchema) -> Optional[InputReadSchema]:
        input_field = InputModel(**input_field.model_dump(), group_id=group_id)
        self._session.add(input_field)
        try:
            await self._session.commit()
        except IntegrityError:
            return
        return InputReadSchema.model_validate(input_field)

    async def get_inputs(self, group_id: UUID) -> list[InputReadSchema]:
        input_fields = await self._session.execute(
            select(InputModel)
            .where(InputModel.group_id == group_id)
            .order_by(InputModel.created_at)
        )
        return [
            InputReadSchema.model_validate(input_field)
            for input_field in input_fields.scalars().all()
        ]

    async def get_input_by_id(self, input_id: UUID) -> Optional[InputReadSchema]:
        input_field = await self._get_input_model_instance(input_id)
        if input_field is None:
            return
        return InputReadSchema.model_validate(input_field)

    async def delete_input(self, input_id: UUID):
        await self._session.execute(
            delete(InputModel)
            .where(InputModel.input_id == input_id)
        )
        await self._session.commit()

    async def set_input_destination_group(
            self,
            input_id: UUID,
            destination_group_id: UUID,
    ) -> Optional[InputReadSchema]:
        input_field = await self._get_input_model_instance(input_id)
        if input_field is None:
            return

        input_field.destination_group_id = destination_group_id
        await self._session.commit()

        return InputReadSchema.model_validate(input_field)
