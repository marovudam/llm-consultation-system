import pytest
import respx
from httpx import Response

from app.services.openrouter_client import call_openrouter

@pytest.mark.asyncio
@respx.mock
async def test_call_openrouter_success() -> None:
    route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(
            status_code=200,
            json={"choices": [{ "message": {"content": "Тестовый ответ"}}]}
        )
    )
    result = await call_openrouter("Тестовый вопрос")
    assert route.called
    assert result == "Тестовый ответ"