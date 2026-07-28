from pinecone import Pinecone

from app.core.config import get_settings

def get_store():
    settings = get_settings()

    store = Pinecone(api_key=settings.pinecore_api_key)
    return store