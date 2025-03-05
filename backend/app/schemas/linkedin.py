from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class LinkedInProfile(BaseModel):
    """Schema for LinkedIn profile data."""
    profile_url: HttpUrl
    full_name: str
    headline: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    location: Optional[str] = None
    about: Optional[str] = None
    experience: Optional[List[Dict[str, Any]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    connections_count: Optional[int] = None
    profile_image_url: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    twitter: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class LinkedInProfileCreate(LinkedInProfile):
    """Schema for creating a LinkedIn profile."""
    pass


class LinkedInProfileUpdate(BaseModel):
    """Schema for updating a LinkedIn profile."""
    headline: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    location: Optional[str] = None
    about: Optional[str] = None
    experience: Optional[List[Dict[str, Any]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    skills: Optional[List[str]] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    connections_count: Optional[int] = None
    profile_image_url: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    twitter: Optional[str] = None


class LinkedInProfileDB(LinkedInProfile):
    """Schema for returning a LinkedIn profile from DB."""
    id: int
    lead_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        orm_mode = True


class LinkedInSearchQuery(BaseModel):
    """Schema for LinkedIn search query."""
    keywords: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    job_title: Optional[str] = None
    connection_level: Optional[str] = None  # 1st, 2nd, 3rd
    max_results: Optional[int] = Field(default=50, ge=1, le=100)


class LinkedInSearchResult(BaseModel):
    """Schema for LinkedIn search result."""
    query: LinkedInSearchQuery
    profiles: List[LinkedInProfile]
    total_results: int
    page: int = 1
    search_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Campaign Schemas
class MessageTemplate(BaseModel):
    """Schema for message template."""
    name: str
    subject: Optional[str] = None
    body: str
    variables: Optional[List[str]] = []
    template_type: str = Field(default="connection", description="Type of template (connection, message, inmail)")


class MessageTemplateCreate(MessageTemplate):
    """Schema for creating a message template."""
    pass


class MessageTemplateUpdate(BaseModel):
    """Schema for updating a message template."""
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    variables: Optional[List[str]] = None
    template_type: Optional[str] = None


class MessageTemplateDB(MessageTemplate):
    """Schema for returning a message template from DB."""
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        orm_mode = True


class CampaignBase(BaseModel):
    """Base schema for campaign."""
    name: str
    description: Optional[str] = None
    schedule_type: str = Field(default="immediate", description="When to send messages (immediate, scheduled, interval)")
    schedule_start: Optional[datetime] = None
    schedule_end: Optional[datetime] = None
    interval_hours: Optional[int] = None
    max_messages_per_day: Optional[int] = Field(default=25, ge=1, le=100)
    status: str = Field(default="draft", description="Status of campaign (draft, active, paused, completed)")


class CampaignCreate(CampaignBase):
    """Schema for creating a campaign."""
    connection_template_id: Optional[int] = None
    follow_up_templates: Optional[List[int]] = []
    target_leads: Optional[List[int]] = []


class CampaignUpdate(BaseModel):
    """Schema for updating a campaign."""
    name: Optional[str] = None
    description: Optional[str] = None
    schedule_type: Optional[str] = None
    schedule_start: Optional[datetime] = None
    schedule_end: Optional[datetime] = None
    interval_hours: Optional[int] = None
    max_messages_per_day: Optional[int] = None
    status: Optional[str] = None
    connection_template_id: Optional[int] = None
    follow_up_templates: Optional[List[int]] = None


class CampaignDB(CampaignBase):
    """Schema for returning a campaign from DB."""
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    connection_template_id: Optional[int] = None
    connection_template: Optional[MessageTemplateDB] = None
    follow_up_templates: Optional[List[MessageTemplateDB]] = []
    stats: Optional[Dict[str, Any]] = None

    class Config:
        """Pydantic config."""
        orm_mode = True


class CampaignLeadBase(BaseModel):
    """Base schema for campaign lead."""
    campaign_id: int
    lead_id: int
    status: str = Field(default="pending", description="Status of the lead in the campaign (pending, sent, responded, completed)")
    current_step: int = Field(default=0, description="Current step in the campaign sequence")


class CampaignLeadCreate(CampaignLeadBase):
    """Schema for adding a lead to a campaign."""
    pass


class CampaignLeadUpdate(BaseModel):
    """Schema for updating a campaign lead."""
    status: Optional[str] = None
    current_step: Optional[int] = None
    notes: Optional[str] = None


class CampaignLeadDB(CampaignLeadBase):
    """Schema for returning a campaign lead from DB."""
    id: int
    created_at: datetime
    updated_at: datetime
    last_contacted_at: Optional[datetime] = None
    next_contact_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        """Pydantic config."""
        orm_mode = True