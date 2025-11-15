"""
Jukeyman Autonomous Media Station (JAMS) - Authentication API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr, Field
from datetime import timedelta
import logging

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user
)
from app.core.config import settings
from app.models.user import User
from app.models.tenant import Tenant

logger = logging.getLogger(__name__)

router = APIRouter()


# Request Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    tenant_domain: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    tenant_domain: str
    role: str = Field("customer", pattern="^(customer|creator)$")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


# Routes

@router.post("/register", response_model=TokenResponse)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    """
    # Get tenant
    result = await db.execute(
        select(Tenant).where(Tenant.domain == request.tenant_domain)
    )
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    # Check if user exists
    result = await db.execute(
        select(User).where(
            User.tenant_id == tenant.id,
            User.email == request.email
        )
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        tenant_id=tenant.id,
        email=request.email,
        hashed_password=get_password_hash(request.password),
        role=request.role,
        credits=100,  # Starting credits
        active=True,
        email_verified=False
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "tenant_id": str(tenant.id), "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "tenant_id": str(tenant.id)}
    )
    
    logger.info(f"User registered: {user.email} ({tenant.name})")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user.to_dict()
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login and get access token
    """
    # Get tenant
    result = await db.execute(
        select(Tenant).where(Tenant.domain == request.tenant_domain)
    )
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    # Get user
    result = await db.execute(
        select(User).where(
            User.tenant_id == tenant.id,
            User.email == request.email
        )
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "tenant_id": str(tenant.id), "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "tenant_id": str(tenant.id)}
    )
    
    logger.info(f"User logged in: {user.email} ({tenant.name})")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user.to_dict()
    )


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information
    """
    return current_user.to_dict()


@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token
    """
    payload = decode_token(refresh_token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    
    # Get user
    result = await db.execute(
        select(User).where(User.id == user_id, User.tenant_id == tenant_id)
    )
    user = result.scalar_one_or_none()
    
    if not user or not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )
    
    # Create new access token
    access_token = create_access_token(
        data={"sub": str(user.id), "tenant_id": str(tenant_id), "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

