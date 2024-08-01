from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.authentication import Authentication
from app.users.models import User
from app.users.schemas import CreateUserSchema, OutputUserSchema


class UserRepo:
    def __init__(self) -> None:
        pass

    def create_user(
        self,
        request_user: CreateUserSchema,
        db: Session,
    ):
        auth = Authentication()
        user_in_db = User(
            username=request_user.username,
            password=auth.hash_password(request_user.password),
            f_name=request_user.f_name,
            l_name=request_user.l_name,
            email=request_user.email,
            role=request_user.role,
        )

        db.add(user_in_db)
        db.commit()
        db.refresh(user_in_db)

        if (
            db.query(User).filter(User.username == request_user.username).first()
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create user",
            )

        return OutputUserSchema.model_validate(user_in_db)

    def get_all_users(
        self,
        db: Session,
    ):
        users_in_db: List[User] = db.query(User).all()

        if len(users_in_db) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users found",
            )

        return [
            OutputUserSchema.model_validate(user_in_db) for user_in_db in users_in_db
        ]
