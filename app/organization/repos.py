from typing import List
from app.organization.models import Organization
from app.organization.schemas import CreateOrganizationSchema, OutputOrganizationSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class OrganizationRepo:
    def __init__(self) -> None:
        pass

    def create_organization(
        self,
        request_org: CreateOrganizationSchema,
        db: Session,
    ):
        org_in_db = Organization(
            name=request_org.name,
            admin_id=request_org.admin_id,
        )

        db.add(org_in_db)
        db.commit()
        db.refresh(org_in_db)

        if (
            db.query(Organization).filter(Organization.name == request_org.name).first()
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create organization",
            )

        return OutputOrganizationSchema.model_validate(org_in_db)

    def get_all_organizations(self, db: Session):
        orgs_in_db: List[Organization] = db.query(Organization).all()

        if len(orgs_in_db) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No organizations found"
            )

        return [
            OutputOrganizationSchema.model_validate(org_in_db)
            for org_in_db in orgs_in_db
        ]
