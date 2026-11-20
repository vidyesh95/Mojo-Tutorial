# backend/app/auth/schema.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    email_verified: int = 0
    image: Optional[str] = None
    role: str = "user"
    created_at: str
    updated_at: str

class Session(BaseModel):
    id: str
    token: str
    user_id: str
    expires_at: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: str
    updated_at: str

class Account(BaseModel):
    id: str
    user_id: str
    account_id: str
    provider_id: str = "credential"
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    password: Optional[str] = None
    created_at: str
    updated_at: str

class SignUpRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class SessionResponse(BaseModel):
    user: User
    session: Session
