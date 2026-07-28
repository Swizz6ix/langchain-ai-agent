import hashlib

from app.rag.indexing.chunks_splitter import splitter

def handbook_chunks(handbook_docs):
    handbook_chunks = splitter.split_documents(handbook_docs)

    for doc in handbook_chunks:
        doc.metadata["doc_id"] = hashlib.sha256(
            f"{doc.metadata['source']}-{doc.metadata['page']}-{doc.page_content}".encode()
        ).hexdigest()

    return handbook_chunks