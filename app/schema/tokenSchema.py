from pydantic import BaseModel
from typing import List

# Token data que contiene los roles del usuario
class TokenData(BaseModel):
    roles: List[str]
