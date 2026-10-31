
from sqlalchemy import select, func

from database import SessionLocal
from models import PromotionRequest


ALLOWED_STATUSES = {
    "Pending",
    "Approved",
    "Rejected",
    "Completed",
}


async def create_promotion_request(
    telegram_id: int,
    service_type: str,
    details: str,
    budget: str
):
    service_type = service_type.strip()
    details = details.strip()
    budget = budget.strip()

    if telegram_id <= 0:
        raise ValueError("Invalid Telegram user ID.")

    if not service_type or not details or not budget:
        raise ValueError("All promotion fields are required.")

    async with SessionLocal() as session:
        request = PromotionRequest(
            telegram_id=telegram_id,
            service_type=service_type[:100],
            details=details[:2000],
            budget=budget[:100],
            status="Pending",
        )

        session.add(request)
        await session.commit()
        await session.refresh(request)

        return request


async def get_promotion_requests(status: str = "Pending"):
    if status not in ALLOWED_STATUSES:
        raise ValueError("Invalid promotion status.")

    async with SessionLocal() as session:
        result = await session.execute(
            select(PromotionRequest)
            .where(PromotionRequest.status == status)
            .order_by(PromotionRequest.created_at.desc())
        )

        return result.scalars().all()


async def get_promotion_count():
    async with SessionLocal() as session:
        result = await session.execute(
            select(func.count(PromotionRequest.id))
        )

        return result.scalar_one()


async def update_promotion_status(
    request_id: int,
    new_status: str
):
    if request_id <= 0 or new_status not in ALLOWED_STATUSES:
        return False

    async with SessionLocal() as session:
        result = await session.execute(
            select(PromotionRequest)
            .where(PromotionRequest.id == request_id)
        )

        request = result.scalar_one_or_none()

        if request is None:
            return False

        request.status = new_status
        await session.commit()

        return True
        
