# Backend/controllers/user_controller.py

from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime

from Backend.models.user_model import (
    UserCreate, UserLogin, UserInDB, UserOut, LoginResponse
)
from Backend.utils.database import users_collection
from Backend.utils.jwt_handler import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def register_user(user_data: UserCreate) -> UserOut:
    # 1) Prevent duplicates
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # 2) Hash & prepare DB model
    db_user = UserInDB(
        name=user_data.name,
        type=user_data.type,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        created_at=datetime.utcnow()
    )

    # 3) Insert & grab generated _id
    result = users_collection.insert_one(db_user.model_dump())
    new_id = str(result.inserted_id)

    # 4) Return public-facing model
    return UserOut(
        id=new_id,
        name=user_data.name,
        type=user_data.type,
        email=user_data.email,
        created_at=db_user.created_at
    )

def login_user(login_data: UserLogin) -> LoginResponse:
    # 1) Fetch user
    user_doc = users_collection.find_one({"email": login_data.email})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    # 2) Verify password
    if not verify_password(login_data.password, user_doc["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3) Build public user object
    user_out = UserOut(
        id=str(user_doc["_id"]),
        name=user_doc["name"],
        type=user_doc["type"],
        email=user_doc["email"],
        created_at=user_doc["created_at"]
    )

    # 4) Issue JWT
    token = create_access_token({"user_id": user_out.id})

    # 5) Return wrapped login response
    return LoginResponse(
        message="Login successful",
        token=token,
        user=user_out
    )
