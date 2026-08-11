from datetime import datetime, timezone
from sqlalchemy import delete
from app.models.refresh_token import RefreshToken

class MaintenanceService:
    def __init__(self, session):
        self.session = session

    async def cleanup_expired_refresh_tokens(self) -> int:
        result = await self.session.execute(
            delete(RefreshToken).where(
                RefreshToken.expires_at <= datetime.now(timezone.utc),
            )
        )

        return result.rowcount or 0


        # run with python -m app.workers.cleanup