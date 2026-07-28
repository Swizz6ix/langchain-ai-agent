from typing import Any

from langchain_pinecone import PineconeVectorStore

from app.rag.indexing.store import get_store

index_name = "company-knowledge"
pc = get_store()
index = pc.Index(index_name)


def get_vector_store(embeddings: Any) -> Any:
    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
    )

    return vector_store
