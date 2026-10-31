from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings
from keyboards import back_button

router = Router()


@router.callback_query(F.data == "support")
async def support_handler(callback: CallbackQuery):

    username = settings.SUPPORT_USERNAME.lstrip("@")

    keyboard = InlineKeyboardBuilder()

    keyboard.button(
        text="💬 Contact Support",
        url=f"https://t.me/{username}"
    )

    keyboard.button(
        text="⬅️ Back to Main Menu",
        callback_data="back_home"
    )

    keyboard.adjust(1)

    await callback.message.edit_text(
        "☎️ <b>Trusted Money Support</b>\n\n"
        "Need help with our services or bot?\n\n"
        "Contact our support account below.\n\n"
        "Support: @TM_24x7_SERVICE\n\n"
        "⚠️ Never share your password, OTP or "
        "Telegram login code with anyone.",
        reply_markup=keyboard.as_markup()
    )

    await callback.answer()
