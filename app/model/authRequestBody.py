from typing import Optional
from pydantic import BaseModel

class AuthRequestBody(BaseModel):
    token: Optional[str]
    source: str
