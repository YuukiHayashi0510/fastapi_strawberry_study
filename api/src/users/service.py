from typing import Optional
from fastapi import HTTPException, status
from models import User
from db import SessionService
from src.auth.hash import Hash


class UserService(SessionService):
    def __init__(self):
        super().__init__()

    def create(self, *, name: str, email: str, password_hash: str) -> User:
        user = User(name=name, email=email, password=password_hash)
        self.save(user)
        return user

    def update(
        self,
        *,
        name: str,
        email: str,
        current_password: str,
        new_password: Optional[str],
        user: User
    ) -> User:
        current_hash = Hash(current_password)

        # Password
        if new_password is None:
            if current_hash.verify_password(hashed_password=user.password) == False:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password is invalid.",
                )
        else:
            new_password_hash = Hash(new_password).get_password_hash()
            user.password = new_password_hash

        user.name = name
        user.email = email
        self.save(user)

        return user

    def delete(self, *, id: int) -> User:
        user = self.find_by_id(id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found."
            )

        self.session.delete(user)

        return user

    def find_by_id(self, id: int):
        return self.session.query(User).where(User.id == id).first()

    @staticmethod
    def find_by_email(self, email: str):
        return self.session.query(User).where(User.email == email).first()
