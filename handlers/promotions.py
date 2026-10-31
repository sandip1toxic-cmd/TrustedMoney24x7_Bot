from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

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
    await state.set_state(PromotionForm.service_type)

    await callback.message.edit_text(
        "📣 <b>Promotion Services</b>\n\n"
        "What would you like to promote?\n\n"
        "Send your service type:\n"
        "Example: Telegram Channel, Group, Bot, Website or Social Media."
    )
    await callback.answer()


@router.message(PromotionForm.service_type)
async def get_service_type(message: Message, state: FSMContext):
    await state.update_data(service_type=message.text)
    await state.set_state(PromotionForm.details)

    await message.answer(
        "📝 Please send your promotion details and official link."
    )


@router.message(PromotionForm.details)
async def get_details(message: Message, state: FSMContext):
    await state.update_data(details=message.text)
    await state.set_state(PromotionForm.budget)

    await message.answer(
        "💰 Please send your estimated budget.\n"
        "If you are unsure, type: Not decided"
    )


@router.message(PromotionForm.budget)
async def get_budget(message: Message, state: FSMContext):
    data = await state.get_data()

    async with SessionLocal() as session:
        request = PromotionRequest(
            telegram_id=message.from_user.id,
            service_type=data["service_type"],
            details=data["details"],
            budget=message.text,
        )

        session.add(request)
        await session.commit()

    await state.clear()

    await message.answer(
        "✅ <b>Promotion Request Submitted!</b>\n\n"
        "Your request has been saved.\n"
        "The owner will review it and contact you if needed.",
        reply_markup=back_button()
    )

    try:
        await message.bot.send_message(
            settings.OWNER_ID,
            "📣 <b>New Promotion Request</b>\n\n"
            f"User ID: <code>{message.from_user.id}</code>\n"
            f"Service: {data['service_type']}\n"
            f"Details: {data['details']}\n"
            f"Budget: {message.text}"
        )
    except Exception:
        pass
