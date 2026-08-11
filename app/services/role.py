from enum import Enum, auto

class Role(Enum):
    OWNER = auto()
    ADMIN = auto()
    MANAGER = auto()
    USER = auto()
    GUEST = auto()

    def __str__(self):
        return self.name

# Generic CRUD fallback
BASE_PERMISSIONS = {
    Role.OWNER: {"create", "read", "update", "delete"},
    Role.ADMIN: {"create", "read", "update", "delete"},
    Role.MANAGER: {"create", "read", "update"},
    Role.USER: {"read", "update"},
    Role.GUEST: {"read"}
}

# Resource-scoped permission
RESOURCE_PERMISSIONS = {
    "invite": {
        Role.OWNER: {"send", "resend_any", "revoke_any", "list", "bulk_send"},
        Role.ADMIN: {"send", "resend_any", "revoke_any", "list", "bulk_send"},
        Role.MANAGER: {"send", "resend_any", "revoke_any", "list"},
        Role.USER: set(),
        Role.GUEST: set(),
    },
    "user": {
        Role.OWNER: {"create", "read", "update", "delete"},
        Role.ADMIN: {"create", "read", "update", "delete"},
        Role.MANAGER: {"read", "update"},
        Role.USER: {"read_own", "update_own"},
        Role.GUEST: {"read"},
    },
    "tenant": {
        Role.OWNER: {"read", "update", "delete"},
        Role.ADMIN: {"read", "update"},
        Role.MANAGER: {"read"},
        Role.USER: {"read"},
        Role.GUEST: {"read"},
    }
}

def _normalize_role(role: Role | str | int) -> Role:
    if isinstance(role, Role):
        return role
    
    if isinstance(role, str):
        return Role[role.upper()]
    
    if isinstance(role, int):
        return Role[role]
    
    raise ValueError(f"Invalid role: {role}")

def has_permission(role: Role | str | int, permission: str, resource: str = "global") -> bool:
    role = _normalize_role(role)

    if resource in RESOURCE_PERMISSIONS:
        permissions = RESOURCE_PERMISSIONS[resource].get(role, set())
        if permission in permissions:
            return True

    if resource == "global":
        return permission.lower() in BASE_PERMISSIONS.get(role, set())

    return False