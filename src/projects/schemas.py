import datetime

from pydantic import BaseModel, Field


class ProjectReadSchema(BaseModel):
    project_id: int
    name: str = Field(max_length=256)
    created_at: datetime.datetime

    model_config = {
        'from_attributes': True,
    }


class ProjectCreateSchema(BaseModel):
    name: str = Field(max_length=256)
