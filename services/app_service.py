from sqlalchemy import select

from database import SessionLocal
from models import AppListing


async def add_app(
    title: str,
    category: str,
    source: str,
    url: str,
    description: str = "",
    risk_status: str = "Unverified",
    launch_date: str | None = None,
):
    async with SessionLocal() as session:
        app = AppListing(
            title=title,
            category=category,
            source=source,
            url=url,
            description=description,
            risk_status=risk_status,
            launch_date=launch_date,
            active=True,
        )

        session.add(app)
        await session.commit()
        await session.refresh(app)

        return app.id


async def get_apps(category: str | None = None):
    async with SessionLocal() as session:
        query = select(AppListing).where(
            AppListing.active.is_(True)
        )

        if category:
            query = query.where(
                AppListing.category == category
            )

        result = await session.execute(
            query.order_by(AppListing.id.desc())
        )

        return result.scalars().all()


async def deactivate_app(app_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(AppListing).where(
                AppListing.id == app_id
            )
        )

        app = result.scalar_one_or_none()

        if app is None:
            return False

        app.active = False
        await session.commit()

        return True
