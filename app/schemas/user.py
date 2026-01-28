from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base fields for user schema."""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    status: Optional[str] = None

class UserOut(UserBase):
    id: int
    status: str
    created_at: Optional[datetime]
    last_login: Optional[datetime]