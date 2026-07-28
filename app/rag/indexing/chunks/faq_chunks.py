import hashlib
from typing import Any

from langchain_core.documents import Document

from app.rag.indexing.chunks_splitter import splitter


def faq_chunks(faq_docs: list[Document]) -> Any:
    faq_chunks = splitter.split_documents(faq_docs)

    for doc in faq_chunks:
        doc.metadata["doc_id"] = hashlib.sha256(
            f"{doc.metadata['source']}-{doc.metadata['page']}-{doc.metadata['section']}-{doc.page_content}".encode()
        ).hexdigest()

    return faq_chunks
