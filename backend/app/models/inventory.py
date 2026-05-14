from sqlalchemy import Column, String, ForeignKey, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Item(Base):
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True)
    description = Column(String)
    price = Column(Float, default=0.0)
    quantity = Column(Integer, default=0)
