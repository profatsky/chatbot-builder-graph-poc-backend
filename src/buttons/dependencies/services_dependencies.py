from typing import Annotated

from fastapi import Depends

from src.buttons.services import ButtonService

ButtonServiceDI = Annotated[ButtonService, Depends(ButtonService)]
