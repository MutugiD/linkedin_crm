from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Lead(Base):
    """Lead model for storing LinkedIn profile data and lead information."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    linkedin_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    profile_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    profile_image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Professional information
    headline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    current_title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    current_company_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("company.id"), index=True, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Contact information
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Lead scoring
    lead_score: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)
    industry_score: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)
    role_score: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)
    revenue_score: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)
    tool_score: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)
    engagement_score: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)

    # Lead qualification
    is_qualified: Mapped[bool] = mapped_column(Boolean, default=False)
    qualification_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Lead management
    pipeline_stage_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("pipeline_stage.id"), nullable=True)
    assigned_to_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)

    # Lead source
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # LinkedIn, Import, Manual, etc.
    source_campaign: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Status flags
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    do_not_contact: Mapped[bool] = mapped_column(Boolean, default=False)

    # Data management
    last_enriched: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    data_quality_score: Mapped[Optional[float]] = mapped_column(Float, default=0, nullable=True)

    # Engagement tracking
    last_contacted: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_replied: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    times_contacted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    times_replied: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    company: Mapped[Optional["Company"]] = relationship("Company", back_populates="leads", foreign_keys=[current_company_id])
    pipeline_stage: Mapped[Optional["PipelineStage"]] = relationship("PipelineStage", back_populates="leads")
    assigned_to: Mapped[Optional["User"]] = relationship("User", back_populates="assigned_leads", foreign_keys=[assigned_to_id])
    created_by: Mapped[Optional["User"]] = relationship("User", back_populates="created_leads", foreign_keys=[created_by_id])
    work_experiences: Mapped[List["WorkExperience"]] = relationship("WorkExperience", back_populates="lead")
    education_experiences: Mapped[List["EducationExperience"]] = relationship("EducationExperience", back_populates="lead")
    skills: Mapped[List["LeadSkill"]] = relationship("LeadSkill", back_populates="lead")
    interactions: Mapped[List["Interaction"]] = relationship("Interaction", back_populates="lead")

    def __repr__(self) -> str:
        return f"<Lead {self.full_name}>"


class PipelineStage(Base):
    """Pipeline stage model for lead management."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Pipeline configuration
    probability: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Conversion probability (%)
    expected_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Expected days in stage

    # Relationships
    leads: Mapped[List["Lead"]] = relationship("Lead", back_populates="pipeline_stage")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<PipelineStage {self.name}>"


class WorkExperience(Base):
    """Work experience model for lead's professional history."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("lead.id"), nullable=False)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("company.id"), nullable=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False)

    # Location
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    lead: Mapped["Lead"] = relationship("Lead", back_populates="work_experiences")
    company: Mapped[Optional["Company"]] = relationship("Company")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<WorkExperience {self.title} at {self.company_name}>"


class EducationExperience(Base):
    """Education experience model for lead's educational history."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("lead.id"), nullable=False)
    school_name: Mapped[str] = mapped_column(String(255), nullable=False)
    degree: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    field_of_study: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    lead: Mapped["Lead"] = relationship("Lead", back_populates="education_experiences")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<EducationExperience {self.degree} at {self.school_name}>"


class LeadSkill(Base):
    """Skill model for lead's professional skills."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("lead.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    endorsement_count: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)

    # Relationships
    lead: Mapped["Lead"] = relationship("Lead", back_populates="skills")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<LeadSkill {self.name}>"


class Interaction(Base):
    """Interaction model for tracking lead interactions."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("lead.id"), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)

    # Interaction details
    interaction_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Email, LinkedIn, Call, etc.
    direction: Mapped[str] = mapped_column(String(20), nullable=False)  # Inbound, Outbound
    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Sentiment analysis
    sentiment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sentiment_label: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # Positive, Negative, Neutral

    # Status
    status: Mapped[str] = mapped_column(String(20), default="Pending")  # Pending, Sent, Failed, Replied

    # Timestamps
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    occurred_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    lead: Mapped["Lead"] = relationship("Lead", back_populates="interactions")
    user: Mapped[Optional["User"]] = relationship("User")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<Interaction {self.interaction_type} with {self.lead_id}>"