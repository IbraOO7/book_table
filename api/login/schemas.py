from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class Users(BaseModel):
    id: int
    phone: str
    password: str
    level: str
    
    model_config = ConfigDict(from_attributes=True)

class CreateUser(BaseModel):
    phone: str
    password: str
    level: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


    