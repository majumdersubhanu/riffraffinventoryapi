from sqlalchemy.orm import Session
from fastapi import status
from fastapi.exceptions import HTTPException

from app.authentication import Authenticator

from app.users.models import UserModel
from app.users.schemas import (
    InputUserModelSchema,
    OutputUserModelSchema,
    UpdateUserModelSchema,
)


class UserRepo:
    def __init__(self) -> None:
        pass

    def create(
        self,
        db: Session,
        user: InputUserModelSchema,
    ):
        hashed_password = Authenticator.get_password_hash(user.password)

        user_in_db = UserModel()

        for key, value in user:
            setattr(user_in_db, key, value)

        setattr(user_in_db, "password", hashed_password)

        db.add(user_in_db)
        db.commit()
        db.refresh(user_in_db)

        return OutputUserModelSchema.model_validate(user_in_db)

    def login(
        self,
        db: Session,
        username: str,
        password: str,
    ):
        user_in_db = db.query(UserModel).filter(UserModel.username == username).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )

        hashed_password: str = str(user_in_db.password)

        is_valid = Authenticator.verify_password(
            plain_password=password,
            hashed_password=hashed_password,
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User credential mismatch",
            )

        return OutputUserModelSchema.model_validate(user_in_db)

    def fetch_user_by_username(
        self,
        db: Session,
        username: str,
    ):
        user_in_db = db.query(UserModel).filter(UserModel.username == username).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )

        return OutputUserModelSchema.model_validate(user_in_db)

    def fetch_user_by_id(
        self,
        db: Session,
        id: int,
    ):
        user_in_db = db.query(UserModel).filter(UserModel.id == id).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return OutputUserModelSchema.model_validate(user_in_db)

    def update_user(
        self,
        db: Session,
        user: UpdateUserModelSchema,
        id: int,
    ):
        user_in_db = db.query(UserModel).filter(UserModel.id == id).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )

        update_data = user.model_dump(exclude_unset=True)

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

        return OutputUserModelSchema.model_validate(user_in_db)