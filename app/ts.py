from app.core.config import get_settings

exp = get_settings().access_token_expire_minutes

print(type(exp))
print(exp)
