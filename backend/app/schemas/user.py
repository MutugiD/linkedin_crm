from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    """Base user schema."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    phone_number: Optional[str] = None
    profile_picture: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    """Schema for creating a user."""
    email: EmailStr
    username: str
    password: str
    full_name: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """Schema for updating a user."""
    password: Optional[str] = None


# Properties to return via API
class User(UserBase):
    """Schema for returning a user."""
    id: int
    email: EmailStr
    username: str
    full_name: str

    class Config:
        """Pydantic config."""
        orm_mode = True


# Properties to return via API for current user
class UserInDB(User):
    """Schema for returning a user with additional DB fields."""
    last_login: Optional[str] = None
    email_verified: bool = False
    created_at: str
    updated_at: str

    class Config:
        """Pydantic config."""
        orm_mode = True


# Role schemas
class RoleBase(BaseModel):
    """Base role schema."""
    name: str
    description: Optional[str] = None
    permissions: Optional[str] = None  # JSON string of permissions


class RoleCreate(RoleBase):
    """Schema for creating a role."""
    pass


class RoleUpdate(RoleBase):
    """Schema for updating a role."""
    name: Optional[str] = None


class Role(RoleBase):
    """Schema for returning a role."""
    id: int
    created_at: str
    updated_at: str

    class Config:
        """Pydantic config."""
        orm_mode = True


# User with roles
class UserWithRoles(User):
    """Schema for returning a user with roles."""
    roles: List[Role] = []

    class Config:
        """Pydantic config."""
        orm_mode = True