from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.buttons.schemas import ButtonReadSchema
from src.inputs.schemas import InputReadSchema


class GroupReadSchema(BaseModel):
    group_id: UUID
    name: str = Field(max_length=256)
    created_at: datetime

    inputs: list[InputReadSchema]
    buttons: list[ButtonReadSchema]

    model_config = {
        'from_attributes': True,
    }


class GroupCreateSchema(BaseModel):
    name: str = Field(max_length=256)
