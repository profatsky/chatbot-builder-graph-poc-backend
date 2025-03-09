from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.inputs.enums import InputType


class InputReadSchema(BaseModel):
    input_id: UUID
    type: InputType
    destination_group_id: Optional[UUID]
    created_at: datetime

    model_config = {
        'from_attributes': True,
    }


class InputCreateSchema(BaseModel):
    type: InputType
