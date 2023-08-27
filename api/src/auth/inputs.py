from typing import Optional
import strawberry


@strawberry.input
class SignUpInput:
    name: Optional[str] = None
    email: str
    password: str


@strawberry.input
class SignInInput:
    email: str
    password: str
