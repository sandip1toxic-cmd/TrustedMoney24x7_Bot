
from sqlalchemy import select

from database import SessionLocal
from models import Loot


async def add_loot(
    title: str,
    description: str,
    url: str,
    end_date: str | None = None,
):
    title = title.strip()
    description = description.strip()
    url = url.strip()

    if not title or not url:
        raise ValueError("Title and URL are required.")

    if not url.startswith(("https://", "http://")):
        raise ValueError("Please provide a valid HTTP or HTTPS URL.")

    async with SessionLocal() as session:
        loot = Loot(
            title=title,
            description=description,
            url=url,
            end_date=end_date.strip() if end_date else None,
            status="Active",
            active=True,
        )

        session.add(loot)
        await session.commit()
        await session.refresh(loot)

        return loot.id


async def get_loots():
    async with SessionLocal() as session:
        result = await session.execute(
            select(Loot)
            .where(
                Loot.active.is_(True),
                Loot.status == "Active"
            )
            .order_by(Loot.id.desc())
        )

        return result.scalars().all()


async def deactivate_loot(loot_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Loot).where(Loot.id == loot_id)
        )

        loot = result.scalar_one_or_none()

        if loot is None:
            return False

        loot.active = False
        loot.status = "Inactive"

        await session.commit()

        return True
        
