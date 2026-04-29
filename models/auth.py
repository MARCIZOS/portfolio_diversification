"""Pydantic models for authentication."""

from pydantic import BaseModel, Field, EmailStr


class UserSignup(BaseModel):
    """User registration request."""
    
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=6, description="Password")


class UserLogin(BaseModel):
    """User login request."""
    
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """User response model (safe to send to client)."""
    
    username: str
    email: str


class TokenResponse(BaseModel):
    """JWT token response."""
    
    access_token: str
    token_type: str = "bearer"
    username: str
