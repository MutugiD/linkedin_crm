from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=List[Any])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    # This is a skeleton - to be implemented
    return []


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create new user.
    """
    # This is a skeleton - to be implemented
    return {"message": "User creation endpoint - to be implemented"}


@router.get("/me", response_model=Any)
async def read_user_me(
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get current user.
    """
    # This is a skeleton - to be implemented
    return {"message": "Current user endpoint - to be implemented"}


@router.put("/me", response_model=Any)
async def update_user_me(
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update current user.
    """
    # This is a skeleton - to be implemented
    return {"message": "Update user endpoint - to be implemented"}


@router.get("/{user_id}", response_model=Any)
async def read_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    # This is a skeleton - to be implemented
    return {"message": f"Get user {user_id} endpoint - to be implemented"}


@router.put("/{user_id}", response_model=Any)
async def update_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a user.
    """
    # This is a skeleton - to be implemented
    return {"message": f"Update user {user_id} endpoint - to be implemented"}


@router.delete("/{user_id}", response_model=Any)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a user.
    """
    # This is a skeleton - to be implemented
    return {"message": f"Delete user {user_id} endpoint - to be implemented"}