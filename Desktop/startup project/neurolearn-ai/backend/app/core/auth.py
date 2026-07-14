from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    return encoded_jwt

def create_refresh_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    
    return encoded_jwt

def decode_token(token: str) -> Optional[Dict]:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError as e:
        logger.error(f"Token decode error: {e}")
        return None

def verify_access_token(token: str) -> Optional[str]:
    """Verify an access token and return user_id"""
    payload = decode_token(token)
    
    if not payload:
        return None
    
    if payload.get("type") != "access":
        logger.warning("Invalid token type: expected access token")
        return None
    
    return payload.get("sub")

def verify_refresh_token(token: str) -> Optional[str]:
    """Verify a refresh token and return user_id"""
    payload = decode_token(token)
    
    if not payload:
        return None
    
    if payload.get("type") != "refresh":
        logger.warning("Invalid token type: expected refresh token")
        return None
    
    return payload.get("sub")

def refresh_access_token(refresh_token: str) -> Optional[Dict]:
    """Refresh an access token using a refresh token"""
    user_id = verify_refresh_token(refresh_token)
    
    if not user_id:
        return None
    
    # Create new access token
    access_token = create_access_token(data={"sub": user_id})
    
    # Optionally create new refresh token (rotation)
    new_refresh_token = create_refresh_token(data={"sub": user_id})
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# FastAPI dependencies
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency to get current user from JWT token"""
    token = credentials.credentials
    user_id = verify_access_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id
