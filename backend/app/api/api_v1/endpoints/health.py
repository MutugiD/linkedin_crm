from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter()


@router.get("/")
async def health_check():
    """
    Check API health.
    """
    return {"status": "healthy", "message": "API is running"}


@router.get("/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """
    Check database connection health.
    """
    try:
        # Try a simple query
        result = await db.execute("SELECT 1")
        if result:
            return {"status": "healthy", "message": "Database connection is working"}
        return {"status": "unhealthy", "message": "Database query failed"}
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
        }