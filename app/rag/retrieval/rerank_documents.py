from typing import Any

from langchain_core.documents import Document
from langsmith import traceable

from app.rag.retrieval.reranker import get_reranker

reranker = get_reranker()


@traceable(run_type="retriever", name="rerank_documents")
def rerank_documents(question: str, docs: list[Document]) -> Any:
    compressed = reranker.compress_documents(
        documents=docs,
        query=question,
    )

    return compressed
