from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {
        "name": "AI Agent API",
        "status": "running"
    }