from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db

router = APIRouter()


@router.post("/login")
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # This is a skeleton - to be implemented
    return {"access_token": "dummy_token", "token_type": "bearer"}


@router.post("/refresh")
async def refresh_token():
    """
    Refresh access token.
    """
    # This is a skeleton - to be implemented
    return {"access_token": "dummy_refreshed_token", "token_type": "bearer"}


@router.post("/register")
async def register():
    """
    Register a new user.
    """
    # This is a skeleton - to be implemented
    return {"message": "User registration endpoint - to be implemented"}