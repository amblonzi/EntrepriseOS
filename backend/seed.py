import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models.base import Base
from app.models.auth import Tenant, User
from app.models.crm import Lead, LeadStatus
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.core.config import settings

async def seed_data():
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
        
    async with SessionLocal() as db:
        # Create Tenant
        tenant = Tenant(name="Inphora Demo", subdomain="demo")
        db.add(tenant)
        await db.flush()
        
        # Create Admin User
        user = User(
            tenant_id=tenant.id,
            email=settings.SEED_ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.SEED_ADMIN_PASSWORD),
            full_name="System Administrator",
            role="admin"
        )
        db.add(user)
        await db.flush()
        
        # Create some Leads
        leads = [
            Lead(tenant_id=tenant.id, first_name="John", last_name="Doe", company="Acme Corp", status=LeadStatus.NEW, estimated_value=5000),
            Lead(tenant_id=tenant.id, first_name="Jane", last_name="Smith", company="Tech Solutions", status=LeadStatus.CONTACTED, estimated_value=12000),
        ]
        db.add_all(leads)
        
        await db.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
