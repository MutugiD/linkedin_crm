"""
Base imports for database models.

This module imports all models to ensure Alembic can detect them.
"""

# Import all models here so Alembic can detect them
from app.db.base_class import Base
from app.models.user import User, Role
from app.models.lead import Lead, PipelineStage, WorkExperience, EducationExperience, LeadSkill, Interaction
from app.models.company import Company, Industry, CompanyLocation
from app.models.outreach import MessageTemplate, MessageSequence, SequenceStep, SequenceEnrollment, EnrollmentStep
from app.models.scraping import ScrapeJob, ProxyServer, UserAgentString, ScrapeItemResult
from app.models.scoring import IcpProfile, ScoringCriteria, ScoringHistory