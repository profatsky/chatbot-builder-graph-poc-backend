from typing import Annotated

from fastapi import Depends

from src.actions.repositories import ActionRepository

ActionRepositoryDI = Annotated[ActionRepository, Depends(ActionRepository)]
