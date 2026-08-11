class DomainError(Exception):
    """Base exception for all domain-level errors."""
    def __init__(self, *args):
        super().__init__(*args)

class EmailAlreadyExistsError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)

class InviteExpiredError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)

class InvalidInviteError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)

class InviteAlreadyAcceptedError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)

class PendingInviteExistsError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)

class UnathorizedTenantAccessError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)

class PermissionDeniedError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)
    

class InviteNotFoundError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)
    

class InviteRevokedError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)
    

class InvalidCredentialsError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)
    

class UserNotFoundError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)
    

class TenantNotFoundError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)
    

class TenantMismatchError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)

class InvalidTokenPayloadError(DomainError):
    def __init__(self, *args):
        super().__init__(*args)