from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api import deps
from app.db.session import get_db
from app.models.inventory import Item

router = APIRouter()

@router.get("/items")
async def read_items(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Item).where(Item.tenant_id == current_user.tenant_id))
    return result.scalars().all()
