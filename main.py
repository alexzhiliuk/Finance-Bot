import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN
from bot.db.database import init_db
from bot.handlers import start, expenses, voice, reports
from bot.middlewares.auth import AuthMiddleware


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(AuthMiddleware())

    dp.include_router(start.router)
    dp.include_router(voice.router)   # voice before expenses so F.voice is checked first
    dp.include_router(expenses.router)
    dp.include_router(reports.router)

    await init_db()
    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
