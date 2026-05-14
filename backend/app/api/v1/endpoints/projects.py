from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api import deps
from app.db.session import get_db
from app.models.projects import Project

router = APIRouter()

@router.get("/")
async def read_projects(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Project).where(Project.tenant_id == current_user.tenant_id))
    return result.scalars().all()
