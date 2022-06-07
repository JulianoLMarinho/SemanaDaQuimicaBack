from typing import Any, List
from repository.testRepository import TestRepository
from fastapi import Depends
from sql.connections import MainConnection

class TestService:
    def __init__(self, conn : MainConnection = Depends(), repository: TestRepository = Depends()):
        self.connection = conn
        self.repo = repository
    
    def get_all(self) -> List[Any]:
        return self.repo.get_all()