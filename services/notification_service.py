
import asyncio

from aiogram import Bot
from services.user_service import get_all_user_ids


async def send_notification(bot: Bot, message: str):
    message = message.strip()

    if not message:
        raise ValueError("Notification message cannot be empty.")

    if len(message) > 4000:
        raise ValueError("Notification message is too long.")

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

        await asyncio.sleep(0.05)

    return {
        "total": len(user_ids),
        "success": success,
        "failed": failed,
    }
    
