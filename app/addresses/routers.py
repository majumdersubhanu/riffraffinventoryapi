from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

from app.db import get_db

from app.addresses.schemas import (
    AddressBaseSchema,
    AddressCreateSchema,
    AddressUpdateSchema,
    OutputAddressModelSchema,
)
from app.addresses.repo import AddressRepo
from app.organizations.repo import OrganizationRepo

from typing import List

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

addr_repo = AddressRepo()
org_repo = OrganizationRepo()


@router.post(
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


@router.get(
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