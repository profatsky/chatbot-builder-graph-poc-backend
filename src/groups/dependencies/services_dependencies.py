from typing import Annotated

from fastapi import Depends

from src.groups.services import GroupService

GroupServiceDI = Annotated[GroupService, Depends(GroupService)]
