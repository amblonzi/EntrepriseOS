from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, text

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
    
    # Conversion Rate
    conversion_rate = 0.0
    if total_leads > 0:
        won_count_result = await db.execute(
            select(func.count(Lead.id)).where(
                Lead.tenant_id == current_user.tenant_id,
                Lead.status == LeadStatus.WON
            )
        )
        won_count = won_count_result.scalar()
        conversion_rate = round((won_count / total_leads) * 100, 1)

    # Revenue Trend (last 7 months)
    trend_result = await db.execute(
        select(
            func.to_char(Lead.created_at, 'Mon').label('month'),
            func.sum(Lead.estimated_value).label('sales'),
            func.count(Lead.id).label('leads'),
            func.min(Lead.created_at).label('min_date')
        ).where(
            Lead.tenant_id == current_user.tenant_id,
            Lead.created_at >= func.now() - text("INTERVAL '7 months'")
        ).group_by(func.to_char(Lead.created_at, 'Mon'))
        .order_by('min_date')
    )
    
    revenue_trend = [
        {"name": row.month, "sales": float(row.sales or 0), "leads": row.leads}
        for row in trend_result.all()
    ]
    
    # Fallback if no trend data yet
    if not revenue_trend:
        revenue_trend = [{"name": "No Data", "sales": 0, "leads": 0}]

    return {
        "total_leads": total_leads,
        "total_revenue": total_revenue,
        "active_deals": active_leads,
        "conversion_rate": conversion_rate,
        "revenue_trend": revenue_trend
    }
