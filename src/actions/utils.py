from typing import Type, Union

from src.actions.enums import ActionType
from src.actions.models import TextMessageActionModel, ImageMessageActionModel
from src.actions.schemas import UnionActionReadSchema, TextMessageActionReadSchema, ImageMessageActionReadSchema

UnionActionModel = Union[
    TextMessageActionModel,
    ImageMessageActionModel,
]


def get_action_model_by_type(action_type: ActionType) -> Type[UnionActionModel]:
    types_to_models = {
        ActionType.TEXT_MESSAGE: TextMessageActionModel,
        ActionType.IMAGE_MESSAGE: ImageMessageActionModel,
    }
    return types_to_models[action_type]


def get_action_schema_by_type(action_type: ActionType) -> Type[UnionActionReadSchema]:
    types_to_schemas = {
        ActionType.TEXT_MESSAGE: TextMessageActionReadSchema,
        ActionType.IMAGE_MESSAGE: ImageMessageActionReadSchema,
    }
    return types_to_schemas[action_type]


def validate_action_from_db(action: UnionActionModel) -> UnionActionReadSchema:
    action_schema = get_action_schema_by_type(action.type)
    return action_schema.model_validate(action)
