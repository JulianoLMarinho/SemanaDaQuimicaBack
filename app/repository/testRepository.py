from typing import Any, List
from model.test import Test
from sql.connections import MainConnection
from fastapi import Depends

class TestRepository:
    def __init__(self, conn : MainConnection = Depends()):
        self.connection = conn

    def get_all(self) -> List[Test]:
        query = "SELECT * FROM test_table"
        kl = self.connection.execute(query)
        ll = [Test.parse_obj(row) for row in kl]
        return ll