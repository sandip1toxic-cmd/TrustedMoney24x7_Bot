
from html import escape

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
            .where(
                Loot.active.is_(True),
                Loot.status == "Active"
            )
            .order_by(Loot.id.desc())
            .limit(10)
        )

        loots = result.scalars().all()

    if not loots:
        await callback.message.edit_text(
            "🎁 <b>Free Loots &amp; Rewards</b>\n\n"
            "No active rewards are available right now.",
            reply_markup=back_button()
        )
        await callback.answer()
        return

    messages = ["🎁 <b>Free Loots &amp; Rewards</b>\n"]

    for loot in loots:
        title = escape(loot.title or "")
        description = escape((loot.description or "")[:200])
        status = escape(loot.status or "Unknown")
        end_date = escape(loot.end_date or "Not specified")
        url = escape(loot.url or "", quote=True)

        messages.append(
            f"🎁 <b>{title}</b>\n"
            f"Details: {description}\n"
            f"Status: {status}\n"
            f"End Date: {end_date}\n"
            f'<a href="{url}">Open Reward</a>\n'
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
    
