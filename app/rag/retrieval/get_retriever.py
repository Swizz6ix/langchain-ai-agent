from functools import lru_cache
from typing import Any

from app.llm.embed_provider import get_embeddings
from app.rag.indexing.vector_store import get_vector_store

vector_store = get_vector_store(get_embeddings())


@lru_cache(maxsize=4)
def get_retriever(source: str | None = None) -> Any:
    kwargs: dict[str, Any] = {"k": 20}

    if source:
        kwargs["filter"] = {"source": source}

    return vector_store.as_retriever(search_type="similarity", search_kwargs=kwargs)
