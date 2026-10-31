import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from database import init_db, close_db

from handlers.user import router as user_router
from handlers.admin import router as admin_router
from handlers.apps import router as apps_router
from handlers.loots import router as loots_router
from handlers.promotions import router as promotions_router
from handlers.support import router as support_router


async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()

    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(apps_router)
    dp.include_router(loots_router)
    dp.include_router(promotions_router)
    dp.include_router(support_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Trusted Money Bot is starting...")

        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())
