from passlib.context import CryptContext
import datetime
from datetime import timedelta
from typing import Optional
import jwt
import os
from fastapi import HTTPException, status

from dotenv import load_dotenv

# Load the .env file with the secrets.
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 15)

# Passlib and bcrypt are used to has plain passwords using secret key
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authenticator:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    # Encode data into 2 tokens: access, and refresh token
    def create_tokens(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode_access = data.copy()
        to_encode_refresh = data.copy()
        expire_access = datetime.datetime.now(datetime.UTC) + (
            expires_delta or timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
        )
        expire_refresh = datetime.datetime.now(datetime.UTC) + timedelta(
            days=float(REFRESH_TOKEN_EXPIRE_DAYS)
        )
        to_encode_access.update({"exp": expire_access})
        to_encode_refresh.update({"exp": expire_refresh})
        access_token = jwt.encode(to_encode_access, SECRET_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(to_encode_refresh, SECRET_KEY, algorithm=ALGORITHM)
        return {"access": access_token, "refresh": refresh_token}

    # Decode the access token to check validity of request
    def decode_access_token(self, token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
