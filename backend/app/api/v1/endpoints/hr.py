from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api import deps
from app.db.session import get_db
from app.models.hr import Employee

router = APIRouter()

@router.get("/employees")
async def read_employees(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Employee).where(Employee.tenant_id == current_user.tenant_id))
    return result.scalars().all()
