import asyncio
import logging

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiohttp import ClientTimeout
from config import TOKEN

from aiogram import Bot, Dispatcher
from app.handlers import router

session = AiohttpSession(api=TelegramAPIServer.from_base("http://localhost:8081", is_local=True), timeout=1800)
bot = Bot(token=TOKEN,
          session=session,
          request_timeout=1800
          )
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Goodbye")
