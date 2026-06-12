from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.db.session import engine
from app.db.base import Base
from app.api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Соединение с базой данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    await engine.dispose()

app = FastAPI(title=settings.APP_NAME,
    description="Защищённый API для взаимодействия с большой языковой моделью",
    lifespan=lifespan)

app.include_router(api_router, tags=["auth"])

@app.get("/health", tags=["health"])
async def health_check():
    """Проверка запуска окружения: статус и окружение"""
    return {"status": "ok", "env": settings.ENV}