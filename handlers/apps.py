from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy import select

from database import SessionLocal
from models import AppListing
from keyboards import app_categories, back_button

router = Router()


@router.callback_query(F.data == "apps")
async def show_app_categories(callback: CallbackQuery):
    await callback.message.edit_text(
        "📱 <b>Earning Applications</b>\n\n"
        "Select an app category:",
        reply_markup=app_categories()
    )
    await callback.answer()


@router.callback_query(F.data.in_([
    "category_playstore",
    "category_website",
    "category_telegram",
    "category_apk",
    "trending",
    "new_apps",
    "risk_alerts"
]))
async def show_apps(callback: CallbackQuery):

    category_map = {
        "category_playstore": "Play Store",
        "category_website": "Website",
        "category_telegram": "Telegram",
        "category_apk": "APK",
    }

    selected = category_map.get(
        callback.data,
        {
            "trending": "Trending",
            "new_apps": "New",
            "risk_alerts": "Risk"
        }.get(callback.data, "Apps")
    )

    async with SessionLocal() as session:

        query = select(AppListing).where(
            AppListing.active.is_(True)
        )

        if callback.data in category_map:
            query = query.where(
                AppListing.category == selected
            )

        elif callback.data == "trending":
            query = query.where(
                AppListing.category == "Trending"
            )

        elif callback.data == "risk_alerts":
            query = query.where(
                AppListing.risk_status != "Verified"
            )

        if callback.data == "new_apps":
            query = query.order_by(
                AppListing.launch_date.desc()
            )
        else:
            query = query.order_by(
                AppListing.id.desc()
            )

        result = await session.execute(
            query.limit(20)
        )

        apps = result.scalars().all()

    if not apps:
        await callback.message.edit_text(
            f"📱 <b>{selected} Apps</b>\n\n"
            "No apps are available in this category yet.",
            reply_markup=back_button()
        )
        await callback.answer()
        return

    lines = [f"📱 <b>{selected} Apps</b>\n"]

    for app in apps:
        lines.append(
            f"• <b>{app.title}</b>\n"
            f"Category: {app.category}\n"
            f"Source: {app.source}\n"
            f"Risk status: {app.risk_status}\n"
            f"Launch date: {app.launch_date or 'Not available'}\n"
            f"Details: {app.description[:250]}\n"
            f"Link: {app.url}\n"
        )

    lines.append(
        "\n⚠️ Earnings are not guaranteed. "
        "Always check app terms and risks."
    )

    await callback.message.edit_text(
        "\n".join(lines),
        reply_markup=back_button(),
        disable_web_page_preview=True
    )

    await callback.answer()
