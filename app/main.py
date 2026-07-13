from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(
    title="Langchain AI Agent"
)

app.include_router(health_router)

def main() -> None:
    print("Hello from langchain-ai-agent!")


if __name__ == "__main__":
    main()
