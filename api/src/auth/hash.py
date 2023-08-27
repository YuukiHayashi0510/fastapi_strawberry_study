from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def __init__(self, password: str):
        self.password = password

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        """Validation"""
        pass_len = len(password)  # 文字数制限
        if pass_len < 8 or pass_len > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters, maximum 20 characters.",
            )
        self.__password = password

    def get_password_hash(self):
        """パスワードのハッシュ化"""
        try:
            return pwd_cxt.hash(self.password)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )

    def verify_password(self, hashed_password):
        """パスワードの検証"""
        try:
            return pwd_cxt.verify(self.password, hashed_password)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            )
