from aiogram import Bot
from services.user_service import get_all_user_ids


async def send_notification(bot: Bot, message: str):
    user_ids = await get_all_user_ids()

    success = 0
    failed = 0

    for user_id in user_ids:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=message
            )
            success += 1

        except Exception:
            failed += 1

    return {
        "total": len(user_ids),
        "success": success,
        "failed": failed,
    }
