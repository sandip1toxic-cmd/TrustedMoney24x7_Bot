from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Join Official Channel",
                    url="https://t.me/Trusted_Money_India"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📣 Promotion Services",
                    callback_data="promotion"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Earning Applications",
                    callback_data="apps"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎁 Free Loots & Rewards",
                    callback_data="loots"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔥 Trending Apps",
                    callback_data="trending"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🆕 New App Launch",
                    callback_data="new_apps"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚠️ Risk Alerts",
                    callback_data="risk_alerts"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 My Account",
                    callback_data="profile"
                )
            ],
            [
                InlineKeyboardButton(
                    text="☎️ Contact Support",
                    callback_data="support"
                )
            ],
        ]
    )


def app_categories():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Play Store Apps",
                    callback_data="category_playstore"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Website Apps",
                    callback_data="category_website"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Telegram Apps",
                    callback_data="category_telegram"
                )
            ],
            [
                InlineKeyboardButton(
                    text="APK Apps",
                    callback_data="category_apk"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Trending Apps",
                    callback_data="trending"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Back",
                    callback_data="back_home"
                )
            ],
        ]
    )


def back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Back to Main Menu",
                    callback_data="back_home"
                )
            ]
        ]
    )


def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Add App",
                    callback_data="admin_add_app"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎁 Add Loot",
                    callback_data="admin_add_loot"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📣 Promotion Requests",
                    callback_data="admin_promotions"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👥 Users",
                    callback_data="admin_users"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Statistics",
                    callback_data="admin_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 Broadcast",
                    callback_data="admin_broadcast"
                )
            ],
        ]
          )
