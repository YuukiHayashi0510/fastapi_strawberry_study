import os
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from models import User
from src.auth.types import Token, TokenEnum
from .hash import Hash
from src.users.service import UserService


SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_LIFETIME_HOURS = 1
REFRESH_TOKEN_LIFETIME_HOURS = 4
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService(UserService):
    def sign_up(self, *, name: str, email: str, password: str) -> Token:
        user = self.find_by_email(email=email)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists."
            )

        password_hash = Hash(password).get_password_hash()
        user = self.create(name=name, email=email, password_hash=password_hash)

        return self.__create_tokens(user)

    def sign_in(self, email: str, password: str) -> Token:
        user = self.find_by_email(self, email=email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found."
            )

        if Hash(password).verify_password(hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is invalid."
            )

        return self.__create_tokens(user)

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        user = self.__get_current_user_from_token(token, TokenEnum.Access)
        return user

    def get_current_user_from_refresh_token(self, token: str = Depends(oauth2_scheme)):
        user = self.__get_current_user_from_token(token, TokenEnum.Refresh)
        return user

    def __create_tokens(self, user: User) -> Token:
        # ペイロード作成
        access_payload = {
            "token_type": "access_token",
            "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_LIFETIME_HOURS),
            "user_id": user.id,
        }
        refresh_payload = {
            "token_type": "refresh_token",
            "exp": datetime.utcnow() + timedelta(hours=REFRESH_TOKEN_LIFETIME_HOURS),
            "user_id": user.id,
        }

        # トークン作成
        try:
            access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")
            refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")

            user.refresh_token = refresh_token
            user.updated_at = datetime.now()
            self.save(user)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def __get_user_from_token(self, token: str, token_type: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except JWTError:
            raise credentials_exception

        if payload["token_type"] != token_type:
            raise credentials_exception

        user = self.find_by_id(payload["user_id"])
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found."
            )

        return user

    def __get_current_user_from_token(self, token: str, token_type: str):
        user = self.__get_user_from_token(token=token, token_type=token_type)

        # リフレッシュトークンの場合、受け取ったものとDBに保存されているものが一致するか確認
        if token_type == TokenEnum.Refresh and user.refresh_token != token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "name": user.name,
            "email": user.email,
        }
