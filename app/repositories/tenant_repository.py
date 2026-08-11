from app.models.tenant import Tenant
from app.repositories.base_repository import BaseRepository

class TenantRepository(BaseRepository[Tenant]):
    model = Tenant