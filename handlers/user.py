from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import settings
from keyboards import main_menu, back_button
from services.user_service import get_or_create_user

router = Router()


async def check_channel_membership(bot, user_id: int) -> bool:
    if not settings.REQUIRE_CHANNEL_JOIN:
        return True

    channel = settings.CHANNEL_ID or settings.CHANNEL_USERNAME

    try:
        member = await bot.get_chat_member(
            chat_id=channel,
            user_id=user_id
        )

        return member.status in (
            "creator",
            "administrator",
            "member"
        )

    except Exception:
        return False


@router.message(CommandStart())
async def start_handler(message: Message):
    is_joined = await check_channel_membership(
        message.bot,
        message.from_user.id
    )

    if not is_joined:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📢 Join Official Channel",
                        url="https://t.me/Trusted_Money_India"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅ Verify Join",
                        callback_data="join_channel"
                    )
                ]
            ]
        )

        await message.answer(
            "👋 Welcome to Trusted Money!\n\n"
            "Please join our official Telegram channel "
            "to access the bot.",
            reply_markup=keyboard
        )
        return

    await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )

    await message.answer(
        f"👋 Welcome, {message.from_user.first_name}!\n\n"
        "💰 Welcome to Trusted Money.\n"
        "Explore apps, rewards, updates and services below.\n\n"
        "⚠️ Earnings are not guaranteed. Always check "
        "app risks before participating.",
        reply_markup=main_menu()
    )


@router.callback_query(F.data == "join_channel")
async def verify_join(callback: CallbackQuery):
    is_joined = await check_channel_membership(
        callback.bot,
        callback.from_user.id
    )

    if is_joined:
        await callback.message.edit_text(
            "✅ Channel verification successful!\n\n"
            "Send /start to open the main menu."
        )
    else:
        await callback.answer(
            "Please join the official channel first.",
            show_alert=True
        )


@router.callback_query(F.data == "back_home")
async def back_home(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 Trusted Money - Main Menu",
        reply_markup=main_menu()
    )
    await callback.answer()


@router.callback_query(F.data == "profile")
async def profile_handler(callback: CallbackQuery):
    user = callback.from_user

    await callback.message.edit_text(
        "👤 <b>Your Profile</b>\n\n"
        f"Name: {user.full_name}\n"
        f"Telegram ID: <code>{user.id}</code>\n"
        f"Username: @{user.username or 'Not Set'}",
        reply_markup=back_button()
    )

    await callback.answer()
