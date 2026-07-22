from typing import Any

from langchain_openrouter import ChatOpenRouter

from app.core.config import get_settings


def get_llm() -> Any:

    settings = get_settings()

    return ChatOpenRouter(
        model_name="openai/gpt-oss-120b",
        temperature=0,
        max_tokens=1024,
        api_key=settings.openrouter_api_key,
    )
