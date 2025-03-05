from fastapi import APIRouter

from app.api.api_v1.endpoints import health, users, auth, scraping, leads, outreach, analytics

api_router = APIRouter()

# Include routers for different endpoints
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(scraping.router, prefix="/scraping", tags=["LinkedIn Scraping"])
api_router.include_router(leads.router, prefix="/leads", tags=["Leads Management"])
api_router.include_router(outreach.router, prefix="/outreach", tags=["Outreach Automation"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])