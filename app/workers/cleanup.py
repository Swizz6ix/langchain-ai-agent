import asyncio
import logging

from app.services.maintenance import MaintenanceService
from app.database.db import AsyncSessionLocal

logger = logging.getLogger(__name__)

async def run() -> None:
    logger.info("Starting clenaup worker")

    async with AsyncSessionLocal() as session:
        service = MaintenanceService(session)
        deleted = await service.cleanup_expired_refresh_tokens()
        await session.commit()

        logger.info(
            "Cleanup complete: deleted %d expired refresh tokens",
            deleted,
        )

if __name__ == "__main__":
    asyncio.run(run())