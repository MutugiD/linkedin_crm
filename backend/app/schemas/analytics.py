from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from pydantic import BaseModel, Field


class TimeFrame(BaseModel):
    """Schema for time frame filtering."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    period: Optional[str] = Field(default="all", description="Predefined period (today, yesterday, this_week, last_week, this_month, last_month, this_year, all)")


class LeadScoringRule(BaseModel):
    """Schema for lead scoring rule."""
    name: str
    description: Optional[str] = None
    field: str = Field(description="Field to apply the rule to (job_title, company, industry, etc.)")
    operator: str = Field(description="Comparison operator (equals, contains, greater_than, less_than, etc.)")
    value: Union[str, int, bool, List[str]]
    score_value: int = Field(description="Score value to add if rule matches")
    is_active: bool = True


class LeadScoringRuleCreate(LeadScoringRule):
    """Schema for creating a lead scoring rule."""
    pass


class LeadScoringRuleUpdate(BaseModel):
    """Schema for updating a lead scoring rule."""
    name: Optional[str] = None
    description: Optional[str] = None
    field: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[Union[str, int, bool, List[str]]] = None
    score_value: Optional[int] = None
    is_active: Optional[bool] = None


class LeadScoringRuleDB(LeadScoringRule):
    """Schema for returning a lead scoring rule from DB."""
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        orm_mode = True


class LeadScoringResult(BaseModel):
    """Schema for lead scoring result."""
    lead_id: int
    total_score: int
    rule_scores: Dict[str, int] = {}
    scoring_timestamp: datetime = Field(default_factory=datetime.utcnow)


class LeadScoringBatch(BaseModel):
    """Schema for batch lead scoring."""
    lead_ids: List[int]
    apply_rules: Optional[List[int]] = None  # Rule IDs to apply, if None apply all active rules


class DashboardStats(BaseModel):
    """Schema for dashboard statistics."""
    total_leads: int = 0
    new_leads_today: int = 0
    active_campaigns: int = 0
    messages_sent_today: int = 0
    responses_received_today: int = 0
    conversion_rate: float = 0.0
    average_response_time: Optional[float] = None
    top_performing_campaigns: List[Dict[str, Any]] = []
    lead_sources_distribution: Dict[str, int] = {}
    daily_activity_trend: List[Dict[str, Any]] = []


class CampaignPerformance(BaseModel):
    """Schema for campaign performance analytics."""
    campaign_id: int
    campaign_name: str
    time_frame: TimeFrame
    messages_sent: int = 0
    responses_received: int = 0
    connections_accepted: int = 0
    connections_rejected: int = 0
    response_rate: float = 0.0
    conversion_rate: float = 0.0
    average_response_time: Optional[float] = None
    leads_by_status: Dict[str, int] = {}
    daily_stats: List[Dict[str, Any]] = []


class UserActivityStats(BaseModel):
    """Schema for user activity statistics."""
    user_id: int
    time_frame: TimeFrame
    leads_created: int = 0
    messages_sent: int = 0
    responses_handled: int = 0
    campaigns_created: int = 0
    templates_created: int = 0
    daily_activity: List[Dict[str, Any]] = []


class LeadAnalytics(BaseModel):
    """Schema for lead analytics."""
    time_frame: TimeFrame
    total_leads: int = 0
    leads_by_source: Dict[str, int] = {}
    leads_by_status: Dict[str, int] = {}
    leads_by_score: Dict[str, int] = {}
    conversion_by_source: Dict[str, float] = {}
    average_time_to_convert: Optional[float] = None
    growth_rate: float = 0.0
    daily_lead_trend: List[Dict[str, Any]] = []


class MessageAnalytics(BaseModel):
    """Schema for message analytics."""
    time_frame: TimeFrame
    total_messages: int = 0
    messages_by_type: Dict[str, int] = {}
    response_rates: Dict[str, float] = {}
    average_response_times: Dict[str, float] = {}
    best_performing_templates: List[Dict[str, Any]] = []
    worst_performing_templates: List[Dict[str, Any]] = []
    message_volume_by_day: List[Dict[str, Any]] = []
    message_volume_by_hour: Dict[int, int] = {}


class AnalyticsExportOptions(BaseModel):
    """Schema for analytics export options."""
    report_type: str = Field(description="Type of report to export (dashboard, campaign, leads, messages)")
    time_frame: TimeFrame
    format: str = Field(default="csv", description="Export format (csv, xlsx, pdf)")
    campaign_id: Optional[int] = None  # For campaign reports
    include_charts: bool = False  # For PDF exports