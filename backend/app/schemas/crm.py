from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.models.crm import LeadStatus

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: LeadStatus = LeadStatus.NEW
    estimated_value: float = 0.0

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class LeadOut(LeadBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True
