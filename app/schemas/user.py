"""User schema definitions."""

from datetime import datetime
from typing import Optional

from app.schemas.base import StructBase


class UserBase(StructBase):
    """Base schema for User model."""

    name: str
    sername: str


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


class UserUpdate(StructBase):
    """Schema for updating an existing user."""

    name: Optional[str] = None
    sername: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """Schema for User model as stored in database."""

    id: int
    password: str
    created_at: datetime
    updated_at: datetime


class UserResponse(UserBase):
    """Schema for User model as stored in database."""

    id: int
    created_at: datetime
    updated_at: datetime
