from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Transaction(Base):
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(String) # INCOME, EXPENSE
    category = Column(String)

class Invoice(Base):
    __table_args__ = (UniqueConstraint('tenant_id', 'invoice_number', name='uq_tenant_invoice_number'),)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    invoice_number = Column(String, nullable=False)
    client_name = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String, default="PENDING") # PENDING, PAID, OVERDUE
    due_date = Column(DateTime)
