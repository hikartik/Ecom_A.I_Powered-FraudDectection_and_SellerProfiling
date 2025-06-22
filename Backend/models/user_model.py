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


class User(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    user_type: Literal["user", "seller", "admin"] = "user"
    created_at: datetime = Field(default_factory=datetime.now)


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    phone: str
    user_type: str
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_type: str
    user_id: str
    full_name: str
