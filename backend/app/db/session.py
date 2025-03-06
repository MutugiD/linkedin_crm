"""
Database session configuration for SQLAlchemy.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create async engine for the database
async_engine = create_async_engine(
    str(settings.DATABASE_URI),
    echo=False,
    future=True,
)

# Create session factory for database sessions
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting DB session.

    Yields:
        AsyncSession: Database session

    Usage:
        ```
        @app.get("/users/")
        async def get_users(db: AsyncSession = Depends(get_db)):
            # Use the db session here
            ...
        ```
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()