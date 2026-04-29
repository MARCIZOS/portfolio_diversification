"""API routes for authentication."""

from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Optional

from models.auth import UserSignup, UserLogin, TokenResponse, UserResponse
from services.auth_service import (
    register_user,
    authenticate_user,
    create_access_token,
    verify_token,
    get_user,
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=TokenResponse)
def signup(user_data: UserSignup) -> dict:
    """Register a new user."""
    try:
        register_user(user_data.username, user_data.email, user_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    
    # Auto-login after signup
    token = create_access_token(user_data.username)
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user_data.username,
    }


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin) -> dict:
    """Authenticate user and return JWT token."""
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    token = create_access_token(user["username"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user["username"],
    }


@router.get("/me", response_model=UserResponse)
def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Get current user info from JWT token."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid scheme")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        ) from e
    
    username = verify_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user
