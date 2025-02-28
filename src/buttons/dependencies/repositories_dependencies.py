from typing import Annotated

from fastapi import Depends

from src.buttons.repositories import ButtonRepository

ButtonRepositoryDI = Annotated[ButtonRepository, Depends(ButtonRepository)]
