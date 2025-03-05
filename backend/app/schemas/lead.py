from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class LeadBase(BaseModel):
    """Base lead schema."""
    full_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    company_website: Optional[HttpUrl] = None
    status: Optional[str] = Field(default="new", description="Status of the lead (new, contacted, qualified, etc.)")
    source: Optional[str] = None
    score: Optional[int] = Field(default=0, ge=0, le=100, description="Lead score from 0-100")
    tags: Optional[List[str]] = []
    notes: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None


class LeadCreate(LeadBase):
    """Schema for creating a lead."""
    pass


class LeadUpdate(BaseModel):
    """Schema for updating a lead."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    company_website: Optional[HttpUrl] = None
    status: Optional[str] = None
    source: Optional[str] = None
    score: Optional[int] = Field(default=None, ge=0, le=100)
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None


class Lead(LeadBase):
    """Schema for returning a lead."""
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_id: int
    assigned_to_id: Optional[int] = None

    class Config:
        """Pydantic config."""
        orm_mode = True


# Lead Activity Schemas
class LeadActivityBase(BaseModel):
    """Base lead activity schema."""
    lead_id: int
    activity_type: str = Field(description="Type of activity (email, call, meeting, note, etc.)")
    details: Optional[str] = None
    outcome: Optional[str] = None


class LeadActivityCreate(LeadActivityBase):
    """Schema for creating a lead activity."""
    pass


class LeadActivityUpdate(BaseModel):
    """Schema for updating a lead activity."""
    activity_type: Optional[str] = None
    details: Optional[str] = None
    outcome: Optional[str] = None


class LeadActivity(LeadActivityBase):
    """Schema for returning a lead activity."""
    id: int
    created_at: datetime
    created_by_id: int

    class Config:
        """Pydantic config."""
        orm_mode = True


# Lead filtering and search
class LeadFilter(BaseModel):
    """Schema for filtering leads."""
    status: Optional[str] = None
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    score_min: Optional[int] = None
    score_max: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    assigned_to_id: Optional[int] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    search_query: Optional[str] = None


# Lead with activity
class LeadWithActivities(Lead):
    """Schema for returning a lead with activities."""
    activities: List[LeadActivity] = []

    class Config:
        """Pydantic config."""
        orm_mode = True


# Lead batch import/export
class LeadBatchImport(BaseModel):
    """Schema for batch importing leads."""
    leads: List[LeadCreate]


class LeadExportOptions(BaseModel):
    """Schema for lead export options."""
    format: str = Field(default="csv", description="Export format (csv, xlsx)")
    include_activities: bool = False
    filter: Optional[LeadFilter] = None