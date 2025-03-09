from typing import Annotated

from fastapi import Depends

from src.inputs.repositories import InputRepository

InputRepositoryDI = Annotated[InputRepository, Depends(InputRepository)]
