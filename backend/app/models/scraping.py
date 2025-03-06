from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class ScrapeJob(Base):
    """Model for tracking LinkedIn scraping jobs."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Profile, Company, Post, Search, etc.
    status: Mapped[str] = mapped_column(
        String(20), default="Pending", nullable=False
    )  # Pending, Running, Completed, Failed

    # Job configuration
    target_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    search_query: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parameters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of parameters
    depth: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # How many levels to scrape
    max_items: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Max items to scrape

    # Execution tracking
    priority: Mapped[int] = mapped_column(Integer, default=5, nullable=False)  # 1-10, lower is higher priority
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Result tracking
    items_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    items_processed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    items_failed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    created_by: Mapped[Optional["User"]] = relationship("User")
    proxy_used_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("proxy_server.id"), nullable=True)
    proxy_used: Mapped[Optional["ProxyServer"]] = relationship("ProxyServer")
    company_target_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("company.id"), nullable=True)
    company_target: Mapped[Optional["Company"]] = relationship("Company")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<ScrapeJob {self.job_type} - {self.status}>"


class ProxyServer(Base):
    """Model for managing proxy servers for scraping."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    password: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    protocol: Mapped[str] = mapped_column(String(10), default="http", nullable=False)

    # Proxy metadata
    country: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    proxy_provider: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Performance tracking
    success_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failure_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_used: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_success: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_failure: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    average_response_time: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Rate limiting
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    block_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<ProxyServer {self.host}:{self.port}>"


class UserAgentString(Base):
    """Model for storing and rotating user agent strings."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_agent: Mapped[str] = mapped_column(String(500), nullable=False)
    browser: Mapped[str] = mapped_column(String(50), nullable=False)
    browser_version: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    os: Mapped[str] = mapped_column(String(50), nullable=False)
    os_version: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    device_type: Mapped[str] = mapped_column(String(20), default="Desktop", nullable=False)

    # Usage tracking
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_used: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<UserAgent {self.browser} {self.browser_version} - {self.os}>"


class ScrapeItemResult(Base):
    """Model for tracking individual items scraped within a job."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    scrape_job_id: Mapped[int] = mapped_column(Integer, ForeignKey("scrape_job.id"), nullable=False)
    item_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Profile, Company, Post, etc.
    status: Mapped[str] = mapped_column(
        String(20), default="Pending", nullable=False
    )  # Pending, Completed, Failed

    # Item details
    linkedin_url: Mapped[str] = mapped_column(String(500), nullable=False)
    linkedin_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    raw_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of raw scraped data

    # Processing tracking
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Result references
    lead_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("lead.id"), nullable=True)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("company.id"), nullable=True)

    # Relationships
    scrape_job: Mapped["ScrapeJob"] = relationship("ScrapeJob")
    lead: Mapped[Optional["Lead"]] = relationship("Lead")
    company: Mapped[Optional["Company"]] = relationship("Company")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<ScrapeItemResult {self.item_type} - {self.status}>"