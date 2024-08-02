from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.organizations.repos import OrganizationRepo
from app.organizations.schemas import OutputOrganizationSchema, CreateOrganizationSchema

org_router = APIRouter(
    tags=["Organizations"],
    prefix="/organizations",
)

org_repo = OrganizationRepo()


@org_router.post(
    path="/",
    status_code=201,
    response_model=OutputOrganizationSchema,
)
def create_organization(
    request_org: CreateOrganizationSchema,
    db: Session = Depends(get_db),
) -> OutputOrganizationSchema:
    output_org = org_repo.create_organization(
        db=db,
        request_org=request_org,
    )

    return output_org


@org_router.get(
    path="/",
    status_code=201,
    response_model=List[OutputOrganizationSchema],
)
def get_all_organization(
    db: Session = Depends(get_db),
) -> List[OutputOrganizationSchema]:
    output_orgs = org_repo.get_all_organizations(
        db=db,
    )

    return output_orgs
