from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api import deps
from app.db.session import get_db
from app.models.finance import Transaction, Invoice
from app.schemas.finance import InvoiceCreate, InvoiceOut, TransactionOut

router = APIRouter()

@router.get("/transactions", response_model=list[TransactionOut])
async def read_transactions(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Transaction).where(Transaction.tenant_id == current_user.tenant_id))
    return result.scalars().all()

@router.get("/invoices", response_model=list[InvoiceOut])
async def read_invoices(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    result = await db.execute(select(Invoice).where(Invoice.tenant_id == current_user.tenant_id))
    return result.scalars().all()

@router.post("/invoices", response_model=InvoiceOut)
async def create_invoice(
    *,
    db: AsyncSession = Depends(get_db),
    invoice_in: InvoiceCreate,
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    invoice = Invoice(
        **invoice_in.model_dump(),
        tenant_id=current_user.tenant_id
    )
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice
