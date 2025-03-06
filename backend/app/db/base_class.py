"""
SQLAlchemy declarative base class for models.
"""

from typing import Any

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    All models should inherit from this class.
    """

    id: Any

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name automatically based on class name.

        Converts camel case to snake case, e.g. UserProfile -> user_profile
        """
        return cls.__name__.lower()

    # Implement equality methods
    def __eq__(self, other: Any) -> bool:
        """
        Compare objects by their primary key.

        Args:
            other: Object to compare with

        Returns:
            True if objects have the same primary key
        """
        if type(self) is not type(other):
            return False
        if not hasattr(self, "id") or not hasattr(other, "id"):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Generate hash based on object's primary key.

        Returns:
            Hash of the object
        """
        return hash(f"{type(self).__name__}:{self.id}")