from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

