
from html import escape

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from config import settings
from keyboards import main_menu, back_button, admin_menu
from services.user_service import get_or_create_user

router = Router()


# UNIVERSAL CANCEL

@router.message(Command("cancel"))
async def cancel_any_form(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer(
            "ℹ️ There is no active operation to cancel."
        )
        return

    await state.clear()

    if message.from_user.id == settings.OWNER_ID:
        await message.answer(
            "❌ Operation cancelled.",
            reply_markup=admin_menu()
        )
    else:
        await message.answer(
            "❌ Operation cancelled.",
            reply_markup=back_button()
        )


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


async def save_user(user):
    return await get_or_create_user(
        telegram_id=user.id,
        username=user.username,
        full_name=user.full_name
    )


# START COMMAND

@router.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user

    is_joined = await check_channel_membership(
        message.bot,
        user.id
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

    await save_user(user)

    await message.answer(
        f"👋 Welcome, {escape(user.first_name)}!\n\n"
        "💰 Welcome to Trusted Money.\n"
        "Explore apps, rewards, updates and services below.\n\n"
        "⚠️ Earnings are not guaranteed. Always check "
        "app risks before participating.",
        reply_markup=main_menu()
    )


# CHANNEL VERIFICATION

@router.callback_query(F.data == "join_channel")
async def verify_join(callback: CallbackQuery):
    user = callback.from_user

    is_joined = await check_channel_membership(
        callback.bot,
        user.id
    )

    if is_joined:
        await save_user(user)

        await callback.message.edit_text(
            f"✅ Welcome, {escape(user.first_name)}!\n\n"
            "Channel verification successful.\n"
            "You can now use Trusted Money.",
            reply_markup=main_menu()
        )

        await callback.answer("Verification successful!")

    else:
        await callback.answer(
            "Please join the official channel first.",
            show_alert=True
        )


# BACK TO HOME

@router.callback_query(F.data == "back_home")
async def back_home(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏠 Trusted Money - Main Menu",
        reply_markup=main_menu()
    )
    await callback.answer()


# USER PROFILE

@router.callback_query(F.data == "profile")
async def profile_handler(callback: CallbackQuery):
    user = callback.from_user

    name = escape(user.full_name or "Unknown")
    username = escape(user.username) if user.username else "Not Set"

    await callback.message.edit_text(
        "👤 <b>Your Profile</b>\n\n"
        f"Name: {name}\n"
        f"Telegram ID: <code>{user.id}</code>\n"
        f"Username: @{username}",
        reply_markup=back_button()
    )

    await callback.answer()
    
