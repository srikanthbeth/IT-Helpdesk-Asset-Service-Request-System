from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# =====================================
# User Schemas
# =====================================

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# =====================================
# Asset Schemas
# =====================================

class AssetCreate(BaseModel):
    asset_name: str
    asset_tag: str
    asset_type: str
    serial_number: str
    status: str


class AssetUpdate(BaseModel):
    asset_name: str
    asset_tag: str
    asset_type: str
    serial_number: str
    status: str


class AssetResponse(BaseModel):
    id: int
    asset_name: str
    asset_tag: str
    asset_type: str
    serial_number: str
    status: str

    class Config:
        from_attributes = True


# =====================================
# Service Request Schemas
# =====================================

class RequestCreate(BaseModel):
    asset_id: int
    issue_title: str
    description: str
    priority: str


class RequestUpdate(BaseModel):
    issue_title: str
    description: str
    priority: str
    status: str


class RequestResponse(BaseModel):
    id: int
    employee_id: int
    asset_id: int
    support_id: Optional[int] = None
    issue_title: str
    description: str
    priority: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# =====================================
# JWT Token Schemas
# =====================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None