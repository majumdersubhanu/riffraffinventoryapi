from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app import authentication as auth
from app.crud import AddressRepo, CustomFieldRepo, OrganizationRepo, UserRepo
import app.models as models
from app.db import engine, get_db
from app.schemas import (
    AddressBaseSchema,
    AddressCreateSchema,
    CustomFieldCreateSchema,
    InputUserModelSchema,
    OrganizationCreateSchema,
    OrganizationUpdateSchema,
    OutputAddressModelSchema,
    OutputCustomFieldModelSchema,
    OutputOrganizationModelSchema,
    OutputUserModelSchema,
    UpdateUserModelSchema,
)
from datetime import timedelta
import jwt
from typing import List

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="RiffRaff Inventory")

app.mount("/static", StaticFiles(directory="static"), name="static")

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def root():
    return {"message": "Welcome to RiffRaff Inventory APIs"}


user_repo = UserRepo()
org_repo = OrganizationRepo()
addr_repo = AddressRepo()
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


# TODO: Typically we should perform a login right after the user has been created, i.e. return the JWT
@app.post("/users", response_model=OutputUserModelSchema, status_code=201)
def register_user(
    request_user: InputUserModelSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = user_repo.create(db=db, user=request_user)

    if user.organization is not None:
        default_org = OrganizationCreateSchema(
            name=user.organization,
        )
    else:
        default_org = OrganizationCreateSchema(name=f"{user.username}'s Organization")

    background_tasks.add_task(create_organization, default_org, db)

    return user


@app.get("/users/me/", response_model=OutputUserModelSchema)
async def fetch_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> OutputUserModelSchema:
    try:
        authenticator = auth.Authenticator()
        payload = authenticator.decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
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


@app.post("/token/refresh")
async def token_refresh(
    token: str,
    db: Session = Depends(get_db),
):
    try:
        authenticator = auth.Authenticator()
        payload = authenticator.decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
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


@app.patch("/users/update/{id}", response_model=OutputUserModelSchema, status_code=200)
async def update_user_profile(
    id: int,
    request_user: UpdateUserModelSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    updated_user = user_repo.update_user(db=db, id=id, user=request_user)

    return updated_user


@app.get(
    "/organizations",
    response_model=List[OutputOrganizationModelSchema],
    status_code=200,
)
async def fetch_organizations(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    orgs = org_repo.fetch_organizations(db=db)

    return orgs


@app.post(
    "/organizations",
    response_model=OutputOrganizationModelSchema,
    status_code=201,
)
async def create_organization(
    request_org: OrganizationCreateSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    org = org_repo.create(db=db, org=request_org)

    return org


@app.post(
    "/address",
    response_model=OutputAddressModelSchema,
    status_code=201,
)
async def create_address(
    request_addr: AddressCreateSchema,
    org_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    addr = addr_repo.create(db=db, org_id=org_id, addr=request_addr)
    return addr


@app.get(
    "/address/{org_id}",
    response_model=List[AddressBaseSchema],
    status_code=200,
)
async def fetch_addresses_for_organization(
    org_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    org = org_repo.fetch_organizations_by_id(
        db=db,
        org_id=org_id,
    )

    if org.addresses is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No addresses listed for the organization",
        )

    return org.addresses


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


@app.patch(
    "/organizations/{org_id}",
    response_model=OutputOrganizationModelSchema,
    status_code=200,
)
async def update_organization_details(
    org_id: int,
    request_org: OrganizationUpdateSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    curr_usr = await fetch_current_user(db=db)
    curr_usr_id = curr_usr.id if curr_usr is OutputUserModelSchema else None
    updated_org = org_repo.update_organization(
        db=db,
        id=org_id,
        org=request_org,
        usr_id=curr_usr_id,
    )

    return updated_org
