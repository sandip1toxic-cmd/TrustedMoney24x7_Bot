
from html import escape

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import settings
from keyboards import admin_menu, back_button

from services.app_service import add_app
from services.loot_service import add_loot
from services.admin_service import (
    get_dashboard_stats,
    get_recent_users,
)
from services.promotion_service import (
    get_promotion_requests,
    update_promotion_status,
)

router = Router()


class AddAppForm(StatesGroup):
    title = State()
    category = State()
    source = State()
    url = State()
    description = State()
    risk_status = State()
    launch_date = State()


class AddLootForm(StatesGroup):
    title = State()
    description = State()
    url = State()
    end_date = State()


def is_owner(user_id: int) -> bool:
    return user_id == settings.OWNER_ID


def admin_back():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Admin Menu",
                    callback_data="admin_home"
                )
            ]
        ]
    )


async def deny_access(callback: CallbackQuery):
    await callback.answer(
        "⛔ You are not authorized.",
        show_alert=True
    )


@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()

    if not is_owner(message.from_user.id):
        await message.answer("⛔ Access denied.")
        return

    await message.answer(
        "🛠 <b>Trusted Money Admin Panel</b>\n\n"
        "Welcome, Owner!\n"
        "Choose an option below:",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "admin_home")
async def admin_home(callback: CallbackQuery, state: FSMContext):
    if not is_owner(callback.from_user.id):
        await deny_access(callback)
        return

    await state.clear()

    await callback.message.edit_text(
        "🛠 <b>Trusted Money Admin Panel</b>\n\n"
        "Choose an option below:",
        reply_markup=admin_menu()
    )
    await callback.answer()


# ADD APP

@router.callback_query(F.data == "add_app")
async def start_add_app(callback: CallbackQuery, state: FSMContext):
    if not is_owner(callback.from_user.id):
        await deny_access(callback)
        return

    await state.clear()
    await state.set_state(AddAppForm.title)

    await callback.message.edit_text(
        "➕ <b>Add New App</b>\n\n"
        "Send the app title.\n"
        "Send /cancel to cancel."
    )
    await callback.answer()


@router.message(AddAppForm.title)
async def app_title(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    if not message.text or not message.text.strip():
        await message.answer("Please send a valid title.")
        return

    await state.update_data(title=message.text.strip()[:200])
    await state.set_state(AddAppForm.category)

    await message.answer(
        "Select category by typing one:\n"
        "Play Store, Website, Telegram, APK"
    )


@router.message(AddAppForm.category)
async def app_category(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    allowed = {
        "play store": "Play Store",
        "website": "Website",
        "telegram": "Telegram",
        "apk": "APK",
    }

    category = (message.text or "").strip().lower()

    if category not in allowed:
        await message.answer(
            "Invalid category. Send: Play Store, Website, Telegram or APK."
        )
        return

    await state.update_data(category=allowed[category])
    await state.set_state(AddAppForm.source)

    await message.answer("Send the app source or developer name.")


@router.message(AddAppForm.source)
async def app_source(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    if not message.text or not message.text.strip():
        await message.answer("Please send a valid source.")
        return

    await state.update_data(source=message.text.strip()[:50])
    await state.set_state(AddAppForm.url)

    await message.answer("Send the official app URL (https://...).")


@router.message(AddAppForm.url)
async def app_url(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    url = (message.text or "").strip()

    if not url.startswith(("https://", "http://")):
        await message.answer("Please send a valid HTTP or HTTPS URL.")
        return

    await state.update_data(url=url[:2000])
    await state.set_state(AddAppForm.description)

    await message.answer("Send a short app description.")


@router.message(AddAppForm.description)
async def app_description(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    await state.update_data(
        description=(message.text or "").strip()[:1000]
    )
    await state.set_state(AddAppForm.risk_status)

    await message.answer(
        "Send risk status:\n"
        "Verified, Unverified or Risky"
    )


@router.message(AddAppForm.risk_status)
async def app_risk(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    allowed = {
        "verified": "Verified",
        "unverified": "Unverified",
        "risky": "Risky",
    }

    risk = (message.text or "").strip().lower()

    if risk not in allowed:
        await message.answer(
            "Please send Verified, Unverified or Risky."
        )
        return

    await state.update_data(risk_status=allowed[risk])
    await state.set_state(AddAppForm.launch_date)

    await message.answer(
        "Send launch date, or type: Not available"
    )


@router.message(AddAppForm.launch_date)
async def save_app(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    data = await state.get_data()
    launch_date = (message.text or "").strip()

    try:
        app_id = await add_app(
            title=data["title"],
            category=data["category"],
            source=data["source"],
            url=data["url"],
            description=data["description"],
            risk_status=data["risk_status"],
            launch_date=(
                None if launch_date.lower() == "not available"
                else launch_date[:30]
            ),
        )
    except ValueError as error:
        await message.answer(f"❌ {escape(str(error))}")
        return
    except Exception:
        await message.answer("❌ Could not save the app.")
        return

    await state.clear()

    await message.answer(
        f"✅ App added successfully!\n\nApp ID: <code>{app_id}</code>",
        reply_markup=admin_back()
    )


# ADD LOOT

@router.callback_query(F.data == "add_loot")
async def start_add_loot(callback: CallbackQuery, state: FSMContext):
    if not is_owner(callback.from_user.id):
        await deny_access(callback)
        return

    await state.clear()
    await state.set_state(AddLootForm.title)

    await callback.message.edit_text(
        "🎁 <b>Add New Loot</b>\n\n"
        "Send the reward title.\n"
        "Send /cancel to cancel."
    )
    await callback.answer()


@router.message(AddLootForm.title)
async def loot_title(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    if not message.text or not message.text.strip():
        await message.answer("Please send a valid title.")
        return

    await state.update_data(title=message.text.strip()[:200])
    await state.set_state(AddLootForm.description)

    await message.answer("Send reward details.")


@router.message(AddLootForm.description)
async def loot_description(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    await state.update_data(
        description=(message.text or "").strip()[:1000]
    )
    await state.set_state(AddLootForm.url)

    await message.answer("Send the official reward URL (https://...).")


@router.message(AddLootForm.url)
async def loot_url(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    url = (message.text or "").strip()

    if not url.startswith(("https://", "http://")):
        await message.answer("Please send a valid HTTP or HTTPS URL.")
        return

    await state.update_data(url=url[:2000])
    await state.set_state(AddLootForm.end_date)

    await message.answer(
        "Send reward end date, or type: Not specified"
    )


@router.message(AddLootForm.end_date)
async def save_loot(message: Message, state: FSMContext):
    if not is_owner(message.from_user.id):
        await state.clear()
        return

    data = await state.get_data()
    end_date = (message.text or "").strip()

    try:
        loot_id = await add_loot(
            title=data["title"],
            description=data["description"],
            url=data["url"],
            end_date=(
                None if end_date.lower() == "not specified"
                else end_date[:50]
            ),
        )
    except ValueError as error:
        await message.answer(f"❌ {escape(str(error))}")
        return
    except Exception:
        await message.answer("❌ Could not save the reward.")
        return

    await state.clear()

    await message.answer(
        f"✅ Loot added successfully!\n\nLoot ID: <code>{loot_id}</code>",
        reply_markup=admin_back()
    )


# PROMOTION REQUESTS

@router.callback_query(F.data == "promotions")
async def show_promotions(callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await deny_access(callback)
        return

    requests = await get_promotion_requests("Pending")

    if not requests:
        await callback.message.edit_text(
            "📣 No pending promotion requests.",
            reply_markup=admin_back()
        )
        await callback.answer()
        return

    for request in requests[:10]:
        text = (
            "📣 <b>Promotion Request</b>\n\n"
            f"Request ID: <code>{request.id}</code>\n"
            f"User ID: <code>{request.telegram_id}</code>\n"
            f"Service: {escape(request.service_type)}\n"
            f"Details: {escape(request.details[:700])}\n"
            f"Budget: {escape(request.budget)}"
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Approve",
                        callback_data=f"promo_approve_{request.id}"
                    ),
                    InlineKeyboardButton(
                        text="❌ Reject",
                        callback_data=f"promo_reject_{request.id}"
                    ),
                ]
            ]
        )

        await callback.message.answer(
            text,
            reply_markup=keyboard
        )

    await callback.message.answer(
        "End of pending requests.",
        reply_markup=admin_back()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("promo_approve_"))
@router.callback_query(F.data.startswith("promo_reject_"))
async def update_promotion(callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await deny_access(callback)
        return

    try:
        action, request_id = callback.data.rsplit("_", 1)
        request_id = int(request_id)
    except (ValueError, AttributeError):
        await callback.answer("Invalid request.", show_alert=True)
        return

    status = "Approved" if action == "promo_approve" else "Rejected"

    updated = await update_promotion_status(request_id, status)

    if not updated:
        await callback.answer(
            "Request not found or already updated.",
            show_alert=True
        )
        return

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer(f"Request {status.lower()}.")


# USERS

@router.callback_query(F.data == "users")
async def show_users(callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await deny_access(callback)
        return

    users = await get_recent_users(10)

    if not users:
        text = "👥 No users found."
    else:
        lines = ["👥 <b>Recent Users</b>\n"]

        for user in users:
            name = escape(user.full_name or "Unknown")
            username = (
                f"@{escape(user.username)}"
                if user.username else "No username"
            )

            lines.append(
                f"• {name}\n"
                f"ID: <code>{user.telegram_id}</code>\n"
                f"Username: {username}\n"
            )

        text = "\n".join(lines)

    await callback.message.edit_text(
        text,
        reply_markup=admin_back()
    )
    await callback.answer()


# STATISTICS

@router.callback_query(F.data == "stats")
async def show_stats(callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await deny_access(callback)
        return

    stats = await get_dashboard_stats()

    await callback.message.edit_text(
        "📊 <b>Trusted Money Dashboard</b>\n\n"
        f"👥 Total Users: {stats['users']}\n"
        f"📱 Active Apps: {stats['apps']}\n"
        f"🎁 Active Loots: {stats['loots']}\n"
        f"📣 Pending Promotions: {stats['pending_promotions']}",
        reply_markup=admin_back()
    )
    await callback.answer()


# BROADCAST

@router.callback_query(F.data == "broadcast")
async def broadcast_notice(callback: CallbackQuery):
    if not is_owner(callback.from_user.id):
        await deny_access(callback)
        return

    await callback.message.edit_text(
        "📢 <b>Broadcast</b>\n\n"
        "Broadcast is temporarily disabled.\n"
        "A user consent and unsubscribe system "
        "must be added before sending bulk messages.",
        reply_markup=admin_back()
    )
    await callback.answer()


# CANCEL

@router.message(Command("cancel"))
async def cancel_admin_form(message: Message, state: FSMContext):
    if await state.get_state() is None:
        return

    await state.clear()

    if is_owner(message.from_user.id):
        await message.answer(
            "❌ Operation cancelled.",
            reply_markup=admin_menu()
        )
    else:
        await message.answer("Operation cancelled.")
        
