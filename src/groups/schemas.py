from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.actions.schemas import UnionActionReadSchema
from src.actions.utils import validate_action_from_db, UnionActionModel
from src.buttons.schemas import ButtonReadSchema
from src.inputs.schemas import InputReadSchema


class GroupReadSchema(BaseModel):
    group_id: UUID
    name: str = Field(max_length=256)
    created_at: datetime

    inputs: list[InputReadSchema]
    buttons: list[ButtonReadSchema]
    actions: list[UnionActionReadSchema]

    @field_validator('actions')
    @classmethod
    def transform_actions(cls, actions: list[UnionActionModel]):
        return [validate_action_from_db(action) for action in actions]

    model_config = {
        'from_attributes': True,
    }


class GroupCreateSchema(BaseModel):
    name: str = Field(max_length=256)
