from typing import Annotated

from fastapi import Depends

from src.inputs.services import InputService

InputServiceDI = Annotated[InputService, Depends(InputService)]
