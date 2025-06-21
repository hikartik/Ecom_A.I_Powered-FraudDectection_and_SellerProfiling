# Backend/routes/user_routes.py

from fastapi import APIRouter, status
from Backend.models.user_model import UserCreate, UserLogin, UserOut, LoginResponse
from Backend.controllers.user_controller import register_user, login_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def register(user: UserCreate):
    return register_user(user)

@router.post(
    "/login",
    response_model=LoginResponse
)
def login(data: UserLogin):
    return login_user(data)
