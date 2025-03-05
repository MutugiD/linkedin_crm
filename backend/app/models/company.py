from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Industry(Base):
    """Industry classification for companies."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    companies: Mapped[List["Company"]] = relationship("Company", back_populates="industry")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Industry {self.name}>"


class Company(Base):
    """Company model for storing LinkedIn company data."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    linkedin_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Company details
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    industry_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("industry.id"), nullable=True)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    company_size_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    company_size_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    headquarters: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Company metrics
    estimated_revenue: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    funding_total: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_funding_round: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Technology data
    tech_stack: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of tech stack

    # Activity data
    last_post_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    linkedin_follower_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Tracking data
    is_customer: Mapped[bool] = mapped_column(Boolean, default=False)
    is_prospect: Mapped[bool] = mapped_column(Boolean, default=True)
    is_competitor: Mapped[bool] = mapped_column(Boolean, default=False)
    is_partner: Mapped[bool] = mapped_column(Boolean, default=False)

    # Data quality
    data_quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_scraped: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_enriched: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    industry: Mapped[Optional["Industry"]] = relationship("Industry", back_populates="companies")
    locations: Mapped[List["CompanyLocation"]] = relationship("CompanyLocation", back_populates="company")
    leads: Mapped[List["Lead"]] = relationship("Lead", back_populates="company")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Company {self.name}>"


class CompanyLocation(Base):
    """Company locations for multi-location companies."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("company.id"), nullable=False)
    location_type: Mapped[str] = mapped_column(String(50), default="Office")  # HQ, Office, etc.
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="locations")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<CompanyLocation {self.city}, {self.country}>"