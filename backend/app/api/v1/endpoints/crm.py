from typing import Any, List
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
        .where(Lead.tenant_id == current_user.tenant_id)
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
        **lead_in.dict(),
        tenant_id=current_user.tenant_id
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead
