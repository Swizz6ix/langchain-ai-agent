from typing import Any

from langchain_cohere import CohereRerank


def get_reranker() -> Any:
    reranker = CohereRerank(model="rerank-v4.0-pro", top_n=5)

    return reranker
