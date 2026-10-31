
from html import escape

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from services.promotion_service import create_promotion_request
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


