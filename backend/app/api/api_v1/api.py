"""
API v1 router module.

This module combines all API endpoint routers for v1.
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import health, users, auth

api_router = APIRouter()

# Add health endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Add authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Add user endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])

# TODO: Add more endpoint routers as they are implemented:
# api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
# api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
# api_router.include_router(scraping.router, prefix="/scraping", tags=["scraping"])
# api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
# api_router.include_router(settings.router, prefix="/settings", tags=["settings"])