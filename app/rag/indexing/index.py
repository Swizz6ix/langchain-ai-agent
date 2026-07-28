from app.rag.indexing.load_documents.load_faq import load_faq
from app.rag.indexing.load_documents.load_handbook import load_handbook
from app.rag.indexing.slip_documents.split_faq import split_faq
from app.rag.indexing.slip_documents.split_handbook import split_handbook
from app.rag.indexing.chunks.faq_chunks import faq_chunks
from app.rag.indexing.chunks.handbook_chunks import handbook_chunks
from app.rag.indexing.vector_store import get_vector_store
from app.llm.embed_provider import get_embeddings

from dotenv import load_dotenv

load_dotenv()

def index():
    faq = load_faq()
    handbook = load_handbook()

    faq_docs = split_faq(faq)
    handbook_docs = split_handbook(handbook)

    fq_chunks = faq_chunks(faq_docs)
    hb_chunks = handbook_chunks(handbook_docs)

    vector_store = get_vector_store(get_embeddings())
    vector_store.add_documents(fq_chunks + hb_chunks)

    print("Index complete")

if __name__ == "__main__":
    index()