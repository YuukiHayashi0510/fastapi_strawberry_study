from enum import Enum
import strawberry


class TokenEnum(str, Enum):
    """TSの従来のEnum相当"""

    Access = "access_token"
    Refresh = "refresh_token"


@strawberry.type
class Token:
    """Token Type"""

    access_token: str
    refresh_token: str
    token_type: str
