from pydantic import BaseModel
from pydantic.types import PositiveInt

class Test(BaseModel):
    id: PositiveInt
    name: str