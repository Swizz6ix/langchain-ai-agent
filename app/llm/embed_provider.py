from typing import Any

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import get_settings


def get_embeddings() -> Any:
    settings = get_settings()

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", api_key=settings.google_api_key
    )
