from src.auth.service import AuthService
from src.auth.inputs import SignUpInput, SignInInput


def sign_up(input: SignUpInput):
    service = AuthService()
    return service.sign_up(**input.__dict__)


def sign_in(input: SignInInput):
    service = AuthService()
    return service.sign_in(**input.__dict__)


def current_user():
    service = AuthService()
    return service.get_current_user()


def current_user_from_refresh():
    service = AuthService()
    return service.get_current_user_from_refresh_token()
