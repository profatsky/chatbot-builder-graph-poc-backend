from typing import Annotated

from fastapi import Depends

from src.groups.repositories import GroupRepository

GroupRepositoryDI = Annotated[GroupRepository, Depends(GroupRepository)]
