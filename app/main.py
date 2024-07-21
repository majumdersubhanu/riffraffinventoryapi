from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import authentication as auth
from app.db import engine, get_db
from app.crud import CustomFieldRepo
import app.models as models
from app.schemas import (
    CustomFieldCreateSchema,
    OutputCustomFieldModelSchema,
)

from app.users.routers import router as user_router
from app.organizations.routers import router as org_router
from app.addresses.routers import router as address_router

from app.users.repo import UserRepo
from app.organizations.repo import OrganizationRepo

from datetime import timedelta
import jwt
from typing import List

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="RiffRaff Inventory")

app.include_router(user_router, tags=["Users"])
app.include_router(org_router, tags=["Organization"])
app.include_router(address_router, tags=["Address"])

app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def root():
    return {"message": "Welcome to RiffRaff Inventory APIs"}


user_repo = UserRepo()
org_repo = OrganizationRepo()
c_fields_repo = CustomFieldRepo()


@app.post("/token")
async def generate_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_repo.login(db, form_data.username, form_data.password)

    access_token_expires = timedelta(
        minutes=float(auth.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    authenticator = auth.Authenticator()

    tokens = authenticator.create_tokens(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": tokens["access"],
        "refresh_token": tokens["refresh"],
        "token_type": "bearer",
    }


@app.post("/token/refresh")
async def token_refresh(
    token: str,
    db: Session = Depends(get_db),
):
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

    access_token_expires = timedelta(minutes=float(auth.ACCESS_TOKEN_EXPIRE_MINUTES))

    tokens = authenticator.create_tokens(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        "access_token": tokens["access"],
        "refresh_token": token,
        "token_type": "bearer",
    }


@app.post(
    "/custom_fields",
    response_model=OutputCustomFieldModelSchema,
    status_code=201,
)
async def create_custom_field(
    request_custom_field: CustomFieldCreateSchema,
    org_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    custom_field = c_fields_repo.create(
        db=db,
        custom_field=request_custom_field,
        org_id=org_id,
    )

    return custom_field


@app.get(
    "/custom_fields/{org_id}",
    response_model=List[OutputCustomFieldModelSchema],
    status_code=201,
)
async def fetch_custom_fields_for_organization(
    org_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    org = org_repo.fetch_organizations_by_id(db=db, org_id=org_id)

    if org.custom_fields is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No custom fields found for organization.",
        )

    return org.custom_fields
