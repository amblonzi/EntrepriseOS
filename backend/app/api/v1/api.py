from fastapi import APIRouter
from app.api.v1.endpoints import auth, crm, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(crm.router, prefix="/crm", tags=["CRM"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
