from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Tenant(Base):
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True, index=True)
    schema_name = Column(String, unique=True) # For schema-based isolation if needed, or just identifier
    
    users = relationship("User", back_populates="tenant")

class User(Base):
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="user") # Simplified for now, will expand to RBAC
    is_active = Column(Boolean, default=True)
    
    tenant = relationship("Tenant", back_populates="users")
