from typing import Annotated

from fastapi import Depends

from src.actions.services import ActionService

ActionServiceDI = Annotated[ActionService, Depends(ActionService)]
