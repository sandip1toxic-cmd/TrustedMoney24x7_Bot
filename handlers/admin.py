from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import settings
from keyboards import admin_menu, back_button

router = Router()


def is_owner(user_id: int) -> bool:
    return user_id == settings.OWNER_ID


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer("⛔ Access denied.")
        return

    await message.answer(
        "🛠 <b>Trusted Money Admin Panel</b>\n\n"
        "Welcome, Owner!\n"
        "Choose an option below:",
        reply_markup=admin_menu()
    )


@router.callback_query(lambda c: c.data.startswith("admin_"))
async def admin_callbacks(callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await callback.answer(
            "⛔ You are not authorized.",
            show_alert=True
        )
        return

    messages = {
        "admin_add_app": "➕ Add App feature will be connected next.",
        "admin_add_loot": "🎁 Add Loot feature will be connected next.",
        "admin_promotions": "📣 Promotion Requests will appear here.",
        "admin_users": "👥 User management will appear here.",
        "admin_stats": "📊 Bot statistics will appear here.",
        "admin_broadcast": "📢 Broadcast feature will be connected next.",
    }

    text = messages.get(
        callback.data,
        "Unknown admin option."
    )

    await callback.message.edit_text(
        text,
        reply_markup=back_button()
    )
    await callback.answer()
