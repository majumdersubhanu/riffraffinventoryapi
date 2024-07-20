from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

from app.db import get_db

from app.users.schemas import OutputUserModelSchema
import app.users.routers as user_router

from app.organizations.schemas import(
    OrganizationCreateSchema,
    OrganizationUpdateSchema,
    OutputOrganizationModelSchema,
)
from app.organizations.repo import OrganizationRepo

from typing import List

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

org_repo = OrganizationRepo()


@router.get(
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


@router.post(
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


@router.patch(
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
    curr_usr = await user_router.fetch_current_user(db=db)
    curr_usr_id = curr_usr.id if curr_usr is OutputUserModelSchema else None
    updated_org = org_repo.update_organization(
        db=db,
        id=org_id,
        org=request_org,
        usr_id=curr_usr_id,
    )

    return updated_org