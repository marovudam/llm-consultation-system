import httpx
from app.core.config import settings


async def call_openrouter(prompt) -> str:
    """Отправка и получение сообщений от модели"""
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "HTTP-Referer": settings.OPENROUTER_SITE_URL,
        "X-Title": settings.OPENROUTER_APP_NAME,
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 500
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.OPENROUTER_BASE_URL}/chat/completions", 
            headers=headers, json=payload, timeout=60.0)
        if response.status_code != 200:
            raise ValueError(f"Ошибка OpenRouter: {response.status_code} - {response.text}")
        data = response.json()
        return data["choices"][0]["message"]["content"]