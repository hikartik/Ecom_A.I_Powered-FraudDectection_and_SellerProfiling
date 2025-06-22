import os
import base64
import hashlib
import json
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a simple JWT-like token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire.isoformat()})
    
    # Create header
    header = {"alg": "HS256", "typ": "JWT"}
    
    # Encode payload and header
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=').decode()
    payload_b64 = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).rstrip(b'=').decode()
    
    # Create signature
    message = f"{header_b64}.{payload_b64}"
    signature = hashlib.sha256((message + SECRET_KEY).encode()).hexdigest()
    signature_b64 = base64.urlsafe_b64encode(signature.encode()).rstrip(b'=').decode()
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_token(token: str) -> dict:
    """Verify a JWT-like token"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(401, "Invalid token format")
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Verify signature
        message = f"{header_b64}.{payload_b64}"
        expected_signature = hashlib.sha256((message + SECRET_KEY).encode()).hexdigest()
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature.encode()).rstrip(b'=').decode()
        
        if signature_b64 != expected_signature_b64:
            raise HTTPException(401, "Invalid token signature")
        
        # Decode payload
        payload_json = base64.urlsafe_b64decode(payload_b64 + '=' * (4 - len(payload_b64) % 4)).decode()
        payload = json.loads(payload_json)
        
        # Check expiration
        exp_str = payload.get("exp")
        if exp_str:
            exp_time = datetime.fromisoformat(exp_str)
            if datetime.utcnow() > exp_time:
                raise HTTPException(401, "Token expired")
        
        user_id: str = payload.get("user_id")
        if not user_id:
            raise HTTPException(401, "Token missing user_id")
        
        return payload
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(401, "Invalid token")

def get_current_user_id(
    creds: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    payload = verify_token(creds.credentials)
    return payload["user_id"]
