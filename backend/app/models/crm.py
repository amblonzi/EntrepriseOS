from sqlalchemy import Column, String, ForeignKey, Enum, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    LOST = "lost"
    WON = "won"

class Lead(Base):
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    company = Column(String)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    estimated_value = Column(Float, default=0.0)
    
    assigned_to_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    assigned_to = relationship("User")
