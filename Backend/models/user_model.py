from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import datetime

# 🔹 Shared fields for all user models
class UserBase(BaseModel):
    name: str
    type: Literal["seller", "admin", "customer"]
    email: EmailStr
    score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)


# 🔹 Used when registering a new user (input model)
class UserCreate(UserBase):
    password: str


# 🔹 Used during login (input model)
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 🔹 Internal model: used to store in DB with hashed password
class UserInDB(UserBase):
    hashed_password: str


# 🔹 Output model: for returning public-safe data (excludes password)
class UserOut(BaseModel):
    id: Optional[str]
    name: str
    type: Literal["seller", "admin", "customer"]
    email: EmailStr
    created_at: datetime


class LoginResponse(BaseModel):
    message: str
    token: str
    user: UserOut
