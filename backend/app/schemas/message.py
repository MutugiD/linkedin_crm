from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    """Base schema for messages."""
    lead_id: int
    campaign_id: Optional[int] = None
    template_id: Optional[int] = None
    message_type: str = Field(description="Type of message (connection, message, inmail)")
    subject: Optional[str] = None
    content: str
    scheduled_time: Optional[datetime] = None


class MessageCreate(MessageBase):
    """Schema for creating a message."""
    pass


class MessageUpdate(BaseModel):
    """Schema for updating a message."""
    subject: Optional[str] = None
    content: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    status: Optional[str] = None


class Message(MessageBase):
    """Schema for returning a message."""
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime] = None
    status: str = Field(default="draft", description="Status of message (draft, scheduled, sent, failed)")
    tracking_data: Optional[Dict[str, Any]] = None

    class Config:
        """Pydantic config."""
        orm_mode = True


class MessageResponse(BaseModel):
    """Schema for message response."""
    message_id: int
    lead_id: int
    response_type: str = Field(description="Type of response (reply, accept, reject)")
    content: Optional[str] = None
    received_at: datetime = Field(default_factory=datetime.utcnow)
    sentiment: Optional[str] = None
    processed: bool = False


class MessageResponseCreate(MessageResponse):
    """Schema for creating a message response."""
    pass


class MessageResponseUpdate(BaseModel):
    """Schema for updating a message response."""
    response_type: Optional[str] = None
    content: Optional[str] = None
    sentiment: Optional[str] = None
    processed: Optional[bool] = None


class MessageResponseDB(MessageResponse):
    """Schema for returning a message response from DB."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        orm_mode = True


class MessageStats(BaseModel):
    """Schema for message statistics."""
    total_sent: int = 0
    total_delivered: int = 0
    total_opened: int = 0
    total_clicked: int = 0
    total_replied: int = 0
    total_accepted: int = 0
    total_rejected: int = 0
    response_rate: float = 0.0
    conversion_rate: float = 0.0
    average_response_time: Optional[float] = None
    time_period: str = "all_time"


class LeadMessagingHistory(BaseModel):
    """Schema for lead messaging history."""
    lead_id: int
    messages: List[Message] = []
    responses: List[MessageResponseDB] = []
    conversation_status: str = "active"
    last_contact: Optional[datetime] = None
    next_scheduled_contact: Optional[datetime] = None

    class Config:
        """Pydantic config."""
        orm_mode = True


class ScheduledMessageQueue(BaseModel):
    """Schema for scheduled message queue."""
    messages: List[Message] = []
    total_count: int = 0
    pending_count: int = 0

    class Config:
        """Pydantic config."""
        orm_mode = True