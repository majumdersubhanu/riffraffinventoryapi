from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

from app import authentication as auth
from app.db import get_db

from app.organizations.schemas import OrganizationCreateSchema
import app.organizations.routers as org_routers

from app.users.schemas import(
    InputUserModelSchema,
    UpdateUserModelSchema,
    OutputUserModelSchema,
)
from app.users.repo import UserRepo

import jwt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_repo = UserRepo()


# TODO: Typically we should perform a login right after the user has been created, i.e. return the JWT
@router.post(
    "/users", 
    response_model=OutputUserModelSchema, 
    status_code=201
)
def register_user(
    request_user: InputUserModelSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> OutputUserModelSchema:
    user = user_repo.create(db=db, user=request_user)

    if user.organization is not None:
        default_org = OrganizationCreateSchema(
            name=user.organization,
        )
    else:
        default_org = OrganizationCreateSchema(name=f"{user.username}'s Organization")

    background_tasks.add_task(org_routers.create_organization, default_org, db)

    return user


@router.get(
    "/users/me/", 
    response_model=OutputUserModelSchema
)
async def fetch_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> OutputUserModelSchema:
    try:
        authenticator = auth.Authenticator()
        payload = authenticator.decode_access_token(token)
        username: str = payload.get("sub")
        if username.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User credential mismatch",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials | details={e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_repo.fetch_user_by_username(db=db, username=username)

    return user


@router.patch(
    "/users/update/{id}", 
    response_model=OutputUserModelSchema, 
    status_code=200
)
async def update_user_profile(
    id: int,
    request_user: UpdateUserModelSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> OutputUserModelSchema:
    updated_user = user_repo.update_user(db=db, id=id, user=request_user)

    return updated_user