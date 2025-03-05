from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class MessageTemplate(Base):
    """Message template for outreach automation."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Connection, Message, InMail, etc.

    # Template metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Performance tracking
    send_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    response_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    positive_sentiment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    created_by: Mapped[Optional["User"]] = relationship("User")
    sequence_steps: Mapped[List["SequenceStep"]] = relationship("SequenceStep", back_populates="template")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<MessageTemplate {self.name}>"


class MessageSequence(Base):
    """Message sequence for multi-step outreach campaigns."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Sequence configuration
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_automated: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_steps: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    # Target criteria
    target_criteria: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of criteria
    min_lead_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Performance tracking
    enrolled_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    response_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    created_by: Mapped[Optional["User"]] = relationship("User")
    steps: Mapped[List["SequenceStep"]] = relationship("SequenceStep", back_populates="sequence")
    enrollments: Mapped[List["SequenceEnrollment"]] = relationship("SequenceEnrollment", back_populates="sequence")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<MessageSequence {self.name}>"


class SequenceStep(Base):
    """Step in a message sequence."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sequence_id: Mapped[int] = mapped_column(Integer, ForeignKey("message_sequence.id"), nullable=False)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey("message_template.id"), nullable=False)

    # Step configuration
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    wait_days: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Conditional logic
    condition_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # None, NoReply, Sentiment, etc.
    condition_value: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Performance tracking
    sent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    response_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    sequence: Mapped["MessageSequence"] = relationship("MessageSequence", back_populates="steps")
    template: Mapped["MessageTemplate"] = relationship("MessageTemplate", back_populates="sequence_steps")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<SequenceStep {self.step_number} in {self.sequence_id}>"


class SequenceEnrollment(Base):
    """Enrollment of a lead in a message sequence."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("lead.id"), nullable=False)
    sequence_id: Mapped[int] = mapped_column(Integer, ForeignKey("message_sequence.id"), nullable=False)

    # Enrollment status
    status: Mapped[str] = mapped_column(String(50), default="Active")  # Active, Paused, Completed, Stopped
    current_step: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Progress tracking
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_step_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    next_step_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Result tracking
    has_replied: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_positive_sentiment: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_negative_sentiment: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    lead: Mapped["Lead"] = relationship("Lead")
    sequence: Mapped["MessageSequence"] = relationship("MessageSequence", back_populates="enrollments")
    steps: Mapped[List["EnrollmentStep"]] = relationship("EnrollmentStep", back_populates="enrollment")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<SequenceEnrollment {self.lead_id} in {self.sequence_id}>"


class EnrollmentStep(Base):
    """Individual step execution for a sequence enrollment."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    enrollment_id: Mapped[int] = mapped_column(Integer, ForeignKey("sequence_enrollment.id"), nullable=False)
    sequence_step_id: Mapped[int] = mapped_column(Integer, ForeignKey("sequence_step.id"), nullable=False)

    # Step status
    status: Mapped[str] = mapped_column(String(50), default="Pending")  # Pending, Sent, Failed, Skipped
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # Execution tracking
    scheduled_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    executed_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Result tracking
    interaction_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("interaction.id"), nullable=True)
    has_reply: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reply_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    enrollment: Mapped["SequenceEnrollment"] = relationship("SequenceEnrollment", back_populates="steps")
    sequence_step: Mapped["SequenceStep"] = relationship("SequenceStep")
    interaction: Mapped[Optional["Interaction"]] = relationship("Interaction")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<EnrollmentStep {self.step_number} for {self.enrollment_id}>"