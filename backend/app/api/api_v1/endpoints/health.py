"""
Health check endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import get_db

router = APIRouter()


@router.get("/ping")
async def health_check():
    """
    Basic health check.

    Returns:
        dict: Health status
    """
    return {"status": "ok", "message": "Service is running"}


@router.get("/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """
    Database health check.

    Args:
        db: Database session

    Returns:
        dict: Database health status
    """
    try:
        # Execute a simple query to check database connection
        result = await db.execute(text("SELECT 1"))
        value = result.scalar()
        if value == 1:
            return {"status": "ok", "message": "Database connection successful"}
        return {"status": "error", "message": "Database returned unexpected value"}
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}