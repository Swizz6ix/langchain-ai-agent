from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.api.health import router as health_router
from app.api.routes import router
from app.api.home import router as root


app = FastAPI(
    title="Langchain AI Agent"
)

app.include_router(
    root
)

app.include_router(
    router,
    prefix="/api/v1"
)

app.include_router(
    health_router
)