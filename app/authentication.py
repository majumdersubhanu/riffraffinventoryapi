from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from fastapi import HTTPException, status

SECRET_KEY = "3ca66e86b78330d748863ca32c976ddc51df7575da7ed9e769fa15566bf19237"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authenticator:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    def create_tokens(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode_access = data.copy()
        to_encode_refresh = data.copy()
        expire_access = datetime.utcnow() + (
            expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        expire_refresh = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode_access.update({"exp": expire_access})
        to_encode_refresh.update({"exp": expire_refresh})
        access_token = jwt.encode(to_encode_access, SECRET_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(to_encode_refresh, SECRET_KEY, algorithm=ALGORITHM)
        return {"access": access_token, "refresh": refresh_token}

    def decode_access_token(self, token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
