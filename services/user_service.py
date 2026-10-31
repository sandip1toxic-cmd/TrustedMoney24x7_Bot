
from sqlalchemy import select, func

from database import SessionLocal
from models import User


async def get_or_create_user(
    telegram_id: int,
    username: str | None,
    full_name: str
):
    if telegram_id <= 0:
        raise ValueError("Invalid Telegram user ID.")

    username = username.strip() if username else None
    full_name = (full_name or "").strip()[:200]

    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )

        user = result.scalar_one_or_none()

        if user:
            user.username = username
            user.full_name = full_name
        else:
            user = User(
                telegram_id=telegram_id,
                username=username,
                full_name=full_name,
            )
            session.add(user)

        await session.commit()
        await session.refresh(user)

        return user


async def get_user(telegram_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )

        return result.scalar_one_or_none()


async def get_user_count():
    async with SessionLocal() as session:
        result = await session.execute(
            select(func.count(User.id))
        )

        return result.scalar_one()


async def get_all_user_ids():
    async with SessionLocal() as session:
        result = await session.execute(
            select(User.telegram_id)
        )

        return result.scalars().all()
        
