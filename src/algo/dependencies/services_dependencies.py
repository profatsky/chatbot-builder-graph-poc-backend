from typing import Annotated

from fastapi import Depends

from src.algo.services import AlgoService

AlgoServiceDI = Annotated[AlgoService, Depends(AlgoService)]
