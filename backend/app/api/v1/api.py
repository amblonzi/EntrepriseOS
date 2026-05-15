from fastapi import APIRouter
from app.api.v1.endpoints import auth, crm, analytics, finance, inventory, hr, projects

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(crm.router, prefix="/crm", tags=["CRM"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(finance.router, prefix="/finance", tags=["Finance"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(hr.router, prefix="/hr", tags=["HR"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
