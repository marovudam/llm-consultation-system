from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from app.core.config import settings
from app.bot.handlers import router

def create_bot_dispatcher() -> tuple[Bot, Dispatcher]:
    """Создание бота и диспетчера, используется при запуске"""
    session = AiohttpSession()
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, session=session)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    return bot, dispatcher
