import asyncio
from app.services.openrouter_client import call_openrouter
from app.core.config import settings
from app.infra.celery_app import celery_app

from aiogram import Bot

# так и не смогла вытащить бота из dispatcher.py :(
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

@celery_app.task(name="app.tasks.llm_request")
def llm_request(chat_id: int, prompt: str) -> dict:
    """Запрос к модели"""
    try:
        result = asyncio.run(call_openrouter(prompt))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot.send_message(chat_id, result))
        loop.close()
        return {"chat_id": chat_id, "response": result, "status": "success"}
    except Exception as e:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot.send_message(chat_id, f" Ошибка: {str(e)}"))
            loop.close()
        except Exception as e:
            pass
        raise
