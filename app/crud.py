from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.authentication import Authenticator
from app.models import UserModel
from app.schemas import (
    InputUserModelSchema,
    OutputUserModelSchema,
    UpdateUserModelSchema,
)

from datetime import datetime


class UserRepo:
    def create(self, db: Session, user: InputUserModelSchema):
        hashed_password = Authenticator.get_password_hash(user.password)
        user_in_db = UserModel(
            username=user.username,
            email=user.email,
            password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            organization=user.organization,
        )
        db.add(user_in_db)
        db.commit()
        db.refresh(user_in_db)
        return OutputUserModelSchema.from_orm(user_in_db)

    def login(self, db: Session, username: str, password: str):
        user_in_db = db.query(UserModel).filter(UserModel.username == username).first()
        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )
        is_valid = Authenticator.verify_password(
            plain_password=password, hashed_password=user_in_db.password
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User credential mismatch",
            )
        return OutputUserModelSchema.from_orm(user_in_db)

    def fetch_user_by_username(self, db: Session, username: str):
        user_in_db = db.query(UserModel).filter(UserModel.username == username).first()
        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )
        return OutputUserModelSchema.from_orm(user_in_db)

    def update_user(self, db: Session, user: UpdateUserModelSchema, id: int):
        user_in_db = db.query(UserModel).filter(UserModel.id == id).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )

        update_data = user.dict(exclude_unset=True)

        try:
            for key, value in update_data.items():
                setattr(user_in_db, key, value)
            db.commit()
            db.refresh(user_in_db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e,
            )

        return OutputUserModelSchema.from_orm(user_in_db)
