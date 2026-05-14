from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Project(Base):
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="PLANNING")
    budget = Column(Float, default=0.0)
