import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.auth import Tenant, User
from app.core.security import get_password_hash
from app.core.config import settings

async def reset_admin():
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Check for tenant
        res = await session.execute(select(Tenant).where(Tenant.subdomain == "demo"))
        tenant = res.scalars().first()
        if not tenant:
            tenant = Tenant(name="Inphora Demo", subdomain="demo")
            session.add(tenant)
            await session.flush()
        
        # Check for any admin user and delete
        res = await session.execute(select(User).where(User.role == "admin"))
        admins = res.scalars().all()
        for admin in admins:
            await session.delete(admin)
        await session.flush()
        
        # Create BOTH .com and .net admin accounts to ensure user can log in
        credentials = [
            ("admin@inphora.com", "admin123"),
            ("admin@inphora.net", "admin123")
        ]
        
        for email, password in credentials:
            new_admin = User(
                tenant_id=tenant.id,
                email=email,
                hashed_password=get_password_hash(password),
                full_name="System Administrator",
                role="admin",
                is_active=True
            )
            session.add(new_admin)
        
        await session.commit()
        print("Admin users created for BOTH @inphora.com and @inphora.net with password admin123")

if __name__ == "__main__":
    asyncio.run(reset_admin())
