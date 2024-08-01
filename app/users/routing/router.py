from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.users.repos import UserRepo
from app.users.schemas import CreateUserSchema, OutputUserSchema

user_router = APIRouter(
    tags=["User"],
    prefix="/users",
)

user_repo = UserRepo()


@user_router.post(
    path="/",
    status_code=201,
    response_model=OutputUserSchema,
)
def create_user(
    request_user: CreateUserSchema,
    db: Session = Depends(get_db),
) -> OutputUserSchema:
    output_user = user_repo.create_user(
        db=db,
        request_user=request_user,
    )

    return output_user


@user_router.get(
    path="/",
    status_code=200,
    response_model=List[OutputUserSchema],
)
def get_all_users(
    db: Session = Depends(get_db),
) -> List[OutputUserSchema]:
    output_users = user_repo.get_all_users(
        db=db,
    )

    return output_users
