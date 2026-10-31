
from html import escape

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import SessionLocal
from models import PromotionRequest
from keyboards import back_button
from config import settings

router = Router()


class PromotionForm(StatesGroup):
    service_type = State()
    details = State()
    budget = State()


@router.callback_query(F.data == "promotion")
async def start_promotion(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(PromotionForm.service_type)

    await callback.message.edit_text(
        "📣 <b>Promotion Services</b>\n\n"
        "What would you like to promote?\n\n"
        "Example: Telegram Channel, Group, Bot, Website or Social Media.\n\n"
        "Send /cancel to cancel."
    )
    await callback.answer()


@router.message(Command("cancel"))
async def cancel_promotion(message: Message, state: FSMContext):
    if await state.get_state() is None:
        return

    await state.clear()
    await message.answer(
        "❌ Promotion request cancelled.",
        reply_markup=back_button()
    )


@router.message(PromotionForm.service_type)
async def get_service_type(message: Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Please send a valid service type.")
        return

    await state.update_data(
        service_type=message.text.strip()[:100]
    )
    await state.set_state(PromotionForm.details)

    await message.answer(
        "📝 Send your promotion details and official link."
    )


@router.message(PromotionForm.details)
async def get_details(message: Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Please send valid promotion details.")
        return

    await state.update_data(
        details=message.text.strip()[:2000]
    )
    await state.set_state(PromotionForm.budget)

    await message.answer(
        "💰 Send your estimated budget.\n"
        "If unsure, type: Not decided"
    )


@router.message(PromotionForm.budget)
async def get_budget(message: Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Please send a valid budget.")
        return

    data = await state.get_data()
    budget = message.text.strip()[:100]

    request = PromotionRequest(
        telegram_id=message.from_user.id,
        service_type=data["service_type"],
        details=data["details"],
        budget=budget,
        status="Pending",
    )

    async with SessionLocal() as session:
        session.add(request)
        await session.commit()

    await state.clear()

    await message.answer(
        "✅ <b>Promotion Request Submitted!</b>\n\n"
        "Your request has been saved.\n"
        "The owner will review it.",
        reply_markup=back_button()
    )

    try:
        await message.bot.send_message(
            settings.OWNER_ID,
            "📣 <b>New Promotion Request</b>\n\n"
            f"User ID: <code>{message.from_user.id}</code>\n"
            f"Service: {escape(data['service_type'])}\n"
            f"Details: {escape(data['details'])}\n"
            f"Budget: {escape(budget)}"
        )
    except Exception:
        pass
        
