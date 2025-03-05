from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ButtonReadSchema(BaseModel):
    button_id: UUID
    text: str = Field(max_length=64)
    payload: str = Field(max_length=64)
    sequence_number: int
    destination_group_id: Optional[UUID]
    created_at: datetime

    model_config = {
        'from_attributes': True,
    }


class ButtonCreateSchema(BaseModel):
    text: str = Field(max_length=64)
    payload: str = Field(max_length=64)


class ButtonUpdateSchema(BaseModel):
    text: str = Field(max_length=64)
    payload: str = Field(max_length=64)
