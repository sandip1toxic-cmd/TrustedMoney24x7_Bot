from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select

from database import SessionLocal
from models import Loot
from keyboards import back_button

router = Router()


@router.callback_query(F.data == "loots")
async def show_loots(callback: CallbackQuery):

    async with SessionLocal() as session:
        result = await session.execute(
            select(Loot)
            .where(Loot.active.is_(True))
            .order_by(Loot.id.desc())
            .limit(20)
        )

        loots = result.scalars().all()

    if not loots:
        await callback.message.edit_text(
            "🎁 <b>Free Loots & Rewards</b>\n\n"
            "No active rewards are available right now.",
            reply_markup=back_button()
        )
        await callback.answer()
        return

    messages = ["🎁 <b>Free Loots & Rewards</b>\n"]

    for loot in loots:
        messages.append(
            f"🎁 <b>{loot.title}</b>\n"
            f"Details: {loot.description[:250]}\n"
            f"Status: {loot.status}\n"
            f"End Date: {loot.end_date or 'Not specified'}\n"
            f"Link: {loot.url}\n"
        )

    messages.append(
        "⚠️ Check the official terms before participating."
    )

    await callback.message.edit_text(
        "\n".join(messages),
        reply_markup=back_button(),
        disable_web_page_preview=True
    )

    await callback.answer()
