from aiogram import Router, types
from aiogram.filters import Command
from app.infra.redis import get_redis
from app.core.jwt import decode_and_validate
from app.tasks.llm_tasks import llm_request

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message) -> None:
    """Стартовое сообщение"""
    await message.answer(
        """Привет!

Для начала работы:
1) зарегистрируйтесь в Auth Service Swagger
2) получите JWT-токен
3) отправьте команду: /token <ваш_jwt_token>"""
    )

@router.message(Command("token"))
async def save_token(message: types.Message) -> None:
    """Получение токена (команда /token)"""
    token = message.text.replace("/token", "").strip()    
    if not token:
        await message.answer("Работа с командой: /token <JWT>")
        return
    try:
        decode_and_validate(token)
    except ValueError as e:
        await message.answer(str(e))
        return
    redis = await get_redis()
    await redis.set(f"token:{message.from_user.id}", token, ex=60 * 60 * 24)
    await message.answer("Получен корректный токен")


@router.message()
async def ask_llm(message: types.Message) -> None:
    """Диалог с ботом без команд"""
    redis = await get_redis()
    token = await redis.get(f"token:{message.from_user.id}")
    if not token:
        await message.answer("Токен не найден. Отправьте, пожалуйста /token <JWT>")
        return
    try:
        decode_and_validate(token)
    except ValueError as e:
        await message.answer(str(e))
        await redis.delete(f"token:{message.from_user.id}")
        return
    llm_request.delay(message.from_user.id, message.text)
    await message.answer("Получаю ответ...")
