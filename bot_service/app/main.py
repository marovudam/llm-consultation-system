from fastapi import FastAPI
import asyncio
from app.core.config import settings
from app.bot.dispatcher import create_bot_dispatcher

app = FastAPI(title=settings.APP_NAME)

@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.APP_NAME}

async def run_bot() -> None:
    bot, dispatcher = create_bot_dispatcher()
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run_bot())