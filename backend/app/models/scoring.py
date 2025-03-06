from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class IcpProfile(Base):
    """Model for Ideal Customer Profile definition."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ICP configuration
    target_industries: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of industries
    target_company_sizes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of company sizes
    target_roles: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of roles
    target_technologies: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of technologies
    target_locations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of locations

    # Scoring weights
    industry_weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    role_weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    revenue_weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    technology_weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    location_weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    # Metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    created_by: Mapped[Optional["User"]] = relationship("User")
    scoring_criteria: Mapped[List["ScoringCriteria"]] = relationship("ScoringCriteria", back_populates="icp_profile")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<IcpProfile {self.name}>"


class ScoringCriteria(Base):
    """Model for individual scoring criteria within an ICP."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    icp_profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("icp_profile.id"), nullable=False)

    # Criteria details
    criteria_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Industry, Role, Revenue, Technology, etc.
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Scoring configuration
    matcher_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Exact, Fuzzy, Range, Contains, etc.
    matcher_value: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string of matching values
    score_value: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    # Metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    icp_profile: Mapped["IcpProfile"] = relationship("IcpProfile", back_populates="scoring_criteria")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<ScoringCriteria {self.criteria_type}:{self.name}>"


class ScoringHistory(Base):
    """Model for tracking lead scoring history."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("lead.id"), nullable=False)
    icp_profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("icp_profile.id"), nullable=False)

    # Scores
    total_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    industry_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    role_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    revenue_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    technology_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    engagement_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Score details
    score_breakdown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of score details

    # Scoring metadata
    score_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    triggered_by: Mapped[str] = mapped_column(String(50), nullable=False)  # System, User, Scheduled, etc.

    # Status changes
    previous_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    new_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    lead: Mapped["Lead"] = relationship("Lead")
    icp_profile: Mapped["IcpProfile"] = relationship("IcpProfile")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<ScoringHistory {self.lead_id} score:{self.total_score}>"