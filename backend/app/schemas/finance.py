from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class InvoiceBase(BaseModel):
    invoice_number: str
    client_name: str
    amount: Decimal
    status: str = "PENDING"
    due_date: Optional[datetime] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    client_name: Optional[str] = None
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

class InvoiceOut(InvoiceBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True

class TransactionOut(BaseModel):
    id: UUID
    tenant_id: UUID
    description: str
    amount: Decimal
    type: Optional[str] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True
