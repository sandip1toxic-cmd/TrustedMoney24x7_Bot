
from sqlalchemy import select, func

from database import SessionLocal
from models import User, AppListing, Loot, PromotionRequest


async def get_dashboard_stats():
    async with SessionLocal() as session:

        users = await session.execute(
            select(func.count(User.id))
        )

        apps = await session.execute(
            select(func.count(AppListing.id))
            .where(AppListing.active.is_(True))
        )

        loots = await session.execute(
            select(func.count(Loot.id))
            .where(Loot.active.is_(True))
        )

        pending = await session.execute(
            select(func.count(PromotionRequest.id))
            .where(PromotionRequest.status == "Pending")
        )

        return {
            "users": users.scalar_one(),
            "apps": apps.scalar_one(),
            "loots": loots.scalar_one(),
            "pending_promotions": pending.scalar_one(),
        }


async def get_recent_users(limit: int = 10):
    limit = max(1, min(limit, 100))

    async with SessionLocal() as session:
        result = await session.execute(
            select(User)
            .order_by(User.joined_at.desc())
            .limit(limit)
        )

        return result.scalars().all()
        
