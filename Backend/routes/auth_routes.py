from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Backend.models.user_model import User, LoginRequest, LoginResponse, UserResponse
from Backend.utils.database import db, users_collection
from Backend.utils.jwt_handler import create_access_token, verify_token
from datetime import datetime, timedelta
from bson import ObjectId
from passlib.context import CryptContext
from typing import Optional

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=dict)
async def register(user_data: User):
    """
    Register a new user with specified user type
    """
    try:
        # Check if email already exists
        existing_user = users_collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password
        hashed_password = pwd_context.hash(user_data.password)

        # Create user document
        user_doc = {
            "full_name": user_data.full_name,
            "email": user_data.email,
            "phone": user_data.phone,
            "password": hashed_password,
            "user_type": user_data.user_type,
            "created_at": datetime.utcnow()
        }

        # Insert user into database
        result = users_collection.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id

        return {
            "message": "User registered successfully",
            "user": {
                "id": str(result.inserted_id),
                "full_name": user_data.full_name,
                "email": user_data.email,
                "user_type": user_data.user_type
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """
    Login user and return JWT token
    """
    try:
        # Find user by email
        user = users_collection.find_one({"email": login_data.email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Verify password
        if not pwd_context.verify(login_data.password, user['password']):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Create access token
        token_data = {
            "user_id": str(user["_id"]),
            "email": user["email"],
            "user_type": user["user_type"]
        }
        access_token = create_access_token(token_data)

        return LoginResponse(
            access_token=access_token,
            user_type=user["user_type"],
            user_id=str(user["_id"]),
            full_name=user["full_name"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.post("/logout")
async def logout():
    """
    Logout endpoint - clears user session
    """
    return {"message": "Logged out successfully"}

# Dependency function to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Get current user information from JWT token
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": str(user["_id"]),
            "full_name": user["full_name"],
            "email": user["email"],
            "phone": user["phone"],
            "user_type": user["user_type"],
            "created_at": user["created_at"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user

# Helper function to get current user ID from token
async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Extract user ID from JWT token
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") 