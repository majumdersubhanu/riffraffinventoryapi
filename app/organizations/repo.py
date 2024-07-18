from typing_extensions import Optional
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.models import CustomFieldModel

from app.organizations.models import OrganizationModel
from app.users.models import UserModel
from app.addresses.models import AddressModel 
from app.organizations.schemas import (
    OrganizationCreateSchema,
    OrganizationUpdateSchema,
    OutputOrganizationModelSchema,
)


class OrganizationRepo:
    def __init__(self) -> None:
        pass

    def create(
        self,
        db: Session,
        org: OrganizationCreateSchema,
    ):
        org_in_db = OrganizationModel()

        for key, value in org:
            setattr(org_in_db, key, value)

        db.add(org_in_db)
        db.commit()
        db.refresh(org_in_db)

        # Adding addresses if any
        if org.addresses is not None:
            for addr in org.addresses:
                db_addr = AddressModel()

                for key, value in addr:
                    setattr(db_addr, key, value)

                setattr(db_addr, "organization_id", org_in_db.id)

                db.add(db_addr)
                db.commit()
                db.refresh(db_addr)

        # Adding custom fields if any
        if org.custom_fields is not None:
            for custom_field in org.custom_fields:
                db_custom_field = CustomFieldModel()

                for key, value in custom_field:
                    setattr(db_custom_field, key, value)

                setattr(db_custom_field, "organization_id", org_in_db.id)

                db.add(db_custom_field)
                db.commit()
                db.refresh(db_custom_field)

        return OutputOrganizationModelSchema.model_validate(org_in_db)

    def fetch_organizations(
        self,
        db: Session,
    ):
        orgs_in_db = db.query(OrganizationModel).all()

        output_orgs_schemas = [
            OutputOrganizationModelSchema.model_validate(org) for org in orgs_in_db
        ]

        return output_orgs_schemas

    def fetch_organizations_by_id(
        self,
        db: Session,
        org_id: int,
    ):
        org_in_db = (
            db.query(OrganizationModel).filter(OrganizationModel.id == org_id).first()
        )

        if org_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        return OutputOrganizationModelSchema.model_validate(org_in_db)

    def update_organization(
        self,
        db: Session,
        id: int,
        usr_id: Optional[int] | None,
        org: OrganizationUpdateSchema,
    ):
        org_in_db = (
            db.query(OrganizationModel).filter(OrganizationModel.id == id).first()
        )

        if org.name is not None:
            user_in_db = db.query(UserModel).filter(UserModel.id == id).first()
            setattr(user_in_db, "organization", org.name)

        if org_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found",
            )

        update_data = org.model_dump(exclude_unset=True)

        try:
            for key, value in update_data.items():
                setattr(org_in_db, key, value)
            db.commit()
            db.refresh(org_in_db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e,
            )

        return OutputOrganizationModelSchema.model_validate(org_in_db)