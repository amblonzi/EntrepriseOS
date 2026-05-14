from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.api import deps
from app.db.session import get_db
from app.models.crm import Lead, LeadStatus

router = APIRouter()

@router.get("/dashboard-summary")
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    # Total Leads
    total_leads_result = await db.execute(
        select(func.count(Lead.id)).where(Lead.tenant_id == current_user.tenant_id)
    )
    total_leads = total_leads_result.scalar()
    
    # Won Leads (Revenue)
    won_leads_result = await db.execute(
        select(func.sum(Lead.estimated_value)).where(
            Lead.tenant_id == current_user.tenant_id,
            Lead.status == LeadStatus.WON
        )
    )
    total_revenue = won_leads_result.scalar() or 0
    
    # Active Leads (not LOST or WON)
    active_leads_result = await db.execute(
        select(func.count(Lead.id)).where(
            Lead.tenant_id == current_user.tenant_id,
            Lead.status.notin_([LeadStatus.LOST, LeadStatus.WON])
        )
    )
    active_leads = active_leads_result.scalar()
    
    return {
        "total_leads": total_leads,
        "total_revenue": total_revenue,
        "active_deals": active_leads,
        "conversion_rate": 12.5, # Placeholder for more complex calculation
        "revenue_trend": [
            {"name": "Jan", "sales": 4000, "leads": 2400},
            {"name": "Feb", "sales": 3000, "leads": 1398},
            {"name": "Mar", "sales": 2000, "leads": 9800},
            {"name": "Apr", "sales": 2780, "leads": 3908},
            {"name": "May", "sales": 1890, "leads": 4800},
            {"name": "Jun", "sales": 2390, "leads": 3800},
            {"name": "Jul", "sales": 3490, "leads": 4300},
        ]
    }
