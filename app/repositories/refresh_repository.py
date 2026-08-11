from app.models.refresh_token import RefreshToken
from app.repositories.base_repository import BaseRepository
from sqlalchemy import select

class RefreshRepository(BaseRepository[RefreshToken]):
    model = RefreshToken

    async def get_by_hash(self, token_hash: str):
        result = await self.session.execute(
            select(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
        )

        return result.scalar_one_or_none()