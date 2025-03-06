from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, HttpUrl, validator


class PaginationParams(BaseModel):
    """Schema for pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")

    @validator("page")
    def check_page(cls, v):
        if v < 1:
            return 1
        return v

    @validator("page_size")
    def check_page_size(cls, v):
        if v < 1:
            return 20
        if v > 100:
            return 100
        return v


class SortParams(BaseModel):
    """Schema for sorting parameters."""
    sort_by: str
    sort_order: str = Field(default="asc", description="Sort order (asc, desc)")

    @validator("sort_order")
    def check_sort_order(cls, v):
        if v.lower() not in ["asc", "desc"]:
            return "asc"
        return v.lower()


class PaginatedResponse(BaseModel):
    """Schema for paginated response."""
    items: List[Any]
    total: int
    page: int
    page_size: int
    pages: int


class SuccessResponse(BaseModel):
    """Schema for success response."""
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    """Schema for error response."""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None


class EmailSettings(BaseModel):
    """Schema for email settings."""
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    use_tls: bool = True
    from_email: EmailStr
    reply_to_email: Optional[EmailStr] = None
    email_signature: Optional[str] = None
    max_emails_per_day: int = 100


class LinkedInSettings(BaseModel):
    """Schema for LinkedIn settings."""
    username: Optional[str] = None
    password: Optional[str] = None
    session_cookie: Optional[str] = None
    li_at_cookie: Optional[str] = None
    jsessionid: Optional[str] = None
    use_proxy: bool = False
    proxy_url: Optional[str] = None
    max_actions_per_day: int = 50
    connection_delay_min: int = 5  # seconds
    connection_delay_max: int = 20  # seconds
    message_delay_min: int = 30  # seconds
    message_delay_max: int = 90  # seconds


class SystemSettings(BaseModel):
    """Schema for system settings."""
    app_name: str = "LinkedIn CRM"
    app_url: HttpUrl
    default_language: str = "en"
    default_timezone: str = "UTC"
    email_settings: Optional[EmailSettings] = None
    linkedin_settings: Optional[LinkedInSettings] = None
    google_analytics_id: Optional[str] = None
    enable_webhooks: bool = False
    webhook_url: Optional[HttpUrl] = None
    webhook_secret: Optional[str] = None
    maintenance_mode: bool = False
    version: str


class SystemSettingsUpdate(BaseModel):
    """Schema for updating system settings."""
    app_name: Optional[str] = None
    app_url: Optional[HttpUrl] = None
    default_language: Optional[str] = None
    default_timezone: Optional[str] = None
    email_settings: Optional[EmailSettings] = None
    linkedin_settings: Optional[LinkedInSettings] = None
    google_analytics_id: Optional[str] = None
    enable_webhooks: Optional[bool] = None
    webhook_url: Optional[HttpUrl] = None
    webhook_secret: Optional[str] = None
    maintenance_mode: Optional[bool] = None


class WebhookEvent(BaseModel):
    """Schema for webhook event."""
    event_type: str = Field(description="Type of event (lead_created, message_sent, etc.)")
    event_data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_id: str


class AuditLogEntry(BaseModel):
    """Schema for audit log entry."""
    user_id: int
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""
        orm_mode = True


class AuditLogFilter(BaseModel):
    """Schema for audit log filtering."""
    user_id: Optional[int] = None
    action: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


class FileUpload(BaseModel):
    """Schema for file upload response."""
    filename: str
    file_size: int
    file_type: str
    upload_path: str
    public_url: Optional[HttpUrl] = None
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)


class AppHealth(BaseModel):
    """Schema for application health check."""
    status: str
    version: str
    database_connection: bool
    redis_connection: Optional[bool] = None
    last_checked: datetime = Field(default_factory=datetime.utcnow)
    uptime_seconds: int
    component_status: Dict[str, bool] = {}
    resource_usage: Optional[Dict[str, Any]] = None


class NotificationBase(BaseModel):
    """Base schema for notifications."""
    user_id: int
    notification_type: str
    title: str
    message: str
    is_read: bool = False
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    action_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    """Schema for creating a notification."""
    pass


class Notification(NotificationBase):
    """Schema for returning a notification."""
    id: int
    created_at: datetime

    class Config:
        """Pydantic config."""
        orm_mode = True


class NotificationUpdate(BaseModel):
    """Schema for updating a notification."""
    is_read: Optional[bool] = None