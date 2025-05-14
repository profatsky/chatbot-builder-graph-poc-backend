import datetime
from typing import Literal, Annotated, Union
from uuid import UUID

from pydantic import BaseModel, Field

from src.actions.enums import ActionType


class ActionIdWithSeqNumber(BaseModel):
    action_id: UUID
    sequence_number: int = Field(ge=1)

    model_config = {
        'from_attributes': True,
    }


class ActionReadSchema(BaseModel):
    action_id: UUID
    sequence_number: int = Field(ge=1)
    created_at: datetime.datetime

    model_config = {
        'from_attributes': True,
    }


# Text message action
class BaseTextMessageActionSchema(BaseModel):
    text: str = Field(max_length=4096)
    type: Literal[ActionType.TEXT_MESSAGE]


class TextMessageActionReadSchema(BaseTextMessageActionSchema, ActionReadSchema):
    pass


class TextMessageActionCreateSchema(BaseTextMessageActionSchema):
    pass


class TextMessageActionUpdateSchema(BaseTextMessageActionSchema):
    pass


# Image message action
class BaseImageMessageActionSchema(BaseModel):
    image_path: str = Field(max_length=4096)
    type: Literal[ActionType.IMAGE_MESSAGE]


class ImageMessageActionReadSchema(BaseImageMessageActionSchema, ActionReadSchema):
    pass


class ImageMessageActionCreateSchema(BaseImageMessageActionSchema):
    pass


class ImageMessageActionUpdateSchema(BaseImageMessageActionSchema):
    pass


UnionActionReadSchema = Annotated[
    Union[
        TextMessageActionReadSchema,
        ImageMessageActionReadSchema,
    ],
    Field(discriminator='type')
]

UnionActionCreateSchema = Annotated[
    Union[
        TextMessageActionCreateSchema,
        ImageMessageActionCreateSchema,
    ],
    Field(discriminator='type')
]

UnionActionUpdateSchema = Annotated[
    Union[
        TextMessageActionUpdateSchema,
        ImageMessageActionUpdateSchema,
    ],
    Field(discriminator='type')
]
