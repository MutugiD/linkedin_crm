# Import all the models, so that Alembic can detect them
# This file should be imported by alembic/env.py

from app.db.base_class import Base  # noqa

# Import models
from app.models.user import Role, User  # noqa
from app.models.company import Company, CompanyLocation, Industry  # noqa
from app.models.lead import (  # noqa
    EducationExperience,
    Interaction,
    Lead,
    LeadSkill,
    PipelineStage,
    WorkExperience,
)
from app.models.outreach import (  # noqa
    EnrollmentStep,
    MessageSequence,
    MessageTemplate,
    SequenceEnrollment,
    SequenceStep,
)
from app.models.scraping import (  # noqa
    ProxyServer,
    ScrapeItemResult,
    ScrapeJob,
    UserAgentString,
)
from app.models.scoring import (  # noqa
    IcpProfile,
    ScoringCriteria,
    ScoringHistory,
)