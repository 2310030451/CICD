from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.auth import create_access_token, create_refresh_token, decode_token
from app.services.firebase_service import verify_firebase_token
from app.services.user_service import UserService
from loguru import logger

router = APIRouter()


class TokenVerifyRequest(BaseModel):
    id_token: str


class TokenVerifyResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str


@router.post("/verify", response_model=TokenVerifyResponse)
async def verify_token(request: TokenVerifyRequest):
    try:
        firebase_user = await verify_firebase_token(request.id_token)
        
        user_service = UserService()
        user = await user_service.get_or_create_user(firebase_user)
        
        access_token = create_access_token(data={"sub": user.firebase_uid, "user_id": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": user.firebase_uid, "user_id": str(user.id)})
        
        logger.info(f"User {user.firebase_uid} verified successfully")
        
        return TokenVerifyResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=str(user.id)
        )
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    try:
        payload = decode_token(request.refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        access_token = create_access_token(data={"sub": payload["sub"], "user_id": payload["user_id"]})
        
        return RefreshTokenResponse(access_token=access_token)
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
