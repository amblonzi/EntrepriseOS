from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.limiter import limiter

app = FastAPI(
    title="Inphora EntrepriseOS API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Unified CRM + ERP Platform API for SMEs in Africa",
    version="0.1.0",
)

# Rate limiting setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set all CORS enabled origins
allowed_origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
if not allowed_origins:
    if settings.ENVIRONMENT == "production":
        # In production we must explicitly set origins to prevent CSRF/CORS issues
        raise RuntimeError("BACKEND_CORS_ORIGINS must be set in production environment")
    else:
        # Development defaults
        allowed_origins = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Inphora EntrepriseOS API", "status": "operational"}
