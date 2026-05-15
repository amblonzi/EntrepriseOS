from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api import deps
from app.db.session import get_db
from app.models.crm import Lead
from app.models.auth import User
from app.schemas.crm import LeadCreate, LeadUpdate, LeadOut

router = APIRouter()

@router.get("/leads", response_model=List[LeadOut])
async def read_leads(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve leads for the current tenant.
    """
    result = await db.execute(
        select(Lead)
        .where(
            Lead.tenant_id == current_user.tenant_id,
            Lead.is_deleted == False
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.post("/leads", response_model=LeadOut)
async def create_lead(
    *,
    db: AsyncSession = Depends(get_db),
    lead_in: LeadCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new lead.
    """
    lead = Lead(
        **lead_in.model_dump(),
        tenant_id=current_user.tenant_id
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead

@router.patch("/leads/{lead_id}", response_model=LeadOut)
async def update_lead(
    *,
    db: AsyncSession = Depends(get_db),
    lead_id: UUID,
    lead_in: LeadUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a lead.
    """
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id)
    )
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    update_data = lead_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lead, field, value)
    
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead

@router.delete("/leads/{lead_id}", response_model=LeadOut)
async def delete_lead(
    *,
    db: AsyncSession = Depends(get_db),
    lead_id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a lead (soft-delete).
    """
    result = await db.execute(
        select(Lead).where(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id)
    )
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Soft delete
    lead.is_deleted = True
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead
