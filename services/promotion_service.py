from sqlalchemy import select, func
from database import SessionLocal
from models import PromotionRequest


async def create_promotion_request(
    telegram_id: int,
    service_type: str,
    details: str,
    budget: str
):
    async with SessionLocal() as session:
        request = PromotionRequest(
            telegram_id=telegram_id,
            service_type=service_type,
            details=details,
            budget=budget,
            status="Pending",
        )

        session.add(request)
        await session.commit()
        await session.refresh(request)

        return request


async def get_promotion_requests(status: str = "Pending"):
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
