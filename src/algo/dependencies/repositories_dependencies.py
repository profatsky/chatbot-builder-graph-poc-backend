from typing import Annotated

from fastapi import Depends

from src.algo.repositories import AlgoRepository

AlgoRepositoryDI = Annotated[AlgoRepository, Depends(AlgoRepository)]
