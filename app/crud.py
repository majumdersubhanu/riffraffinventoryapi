from typing_extensions import Optional
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.authentication import Authenticator
from app.models import (
    UserModel,
    OrganizationModel,
    AddressModel,
    CustomFieldModel,
)
from app.schemas import (
    AddressCreateSchema,
    CustomFieldCreateSchema,
    InputUserModelSchema,
    OrganizationUpdateSchema,
    OutputAddressModelSchema,
    OutputOrganizationModelSchema,
    OutputUserModelSchema,
    UpdateUserModelSchema,
    OrganizationCreateSchema,
)


class UserRepo:
    def __init__(self) -> None:
        pass

    def create(
        self,
        db: Session,
        user: InputUserModelSchema,
    ):
        hashed_password = Authenticator.get_password_hash(user.password)

        user_in_db = UserModel()

        for key, value in user:
            setattr(user_in_db, key, value)

        setattr(user_in_db, "password", hashed_password)

        db.add(user_in_db)
        db.commit()
        db.refresh(user_in_db)

        return OutputUserModelSchema.from_orm(user_in_db)

    def login(
        self,
        db: Session,
        username: str,
        password: str,
    ):
        user_in_db = db.query(UserModel).filter(UserModel.username == username).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )

        is_valid = Authenticator.verify_password(
            plain_password=password, hashed_password=user_in_db.password
        )

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User credential mismatch",
            )

        return OutputUserModelSchema.from_orm(user_in_db)

    def fetch_user_by_username(
        self,
        db: Session,
        username: str,
    ):
        user_in_db = db.query(UserModel).filter(UserModel.username == username).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )

        return OutputUserModelSchema.from_orm(user_in_db)

    def fetch_user_by_id(
        self,
        db: Session,
        id: int,
    ):
        user_in_db = db.query(UserModel).filter(UserModel.id == id).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return OutputUserModelSchema.from_orm(user_in_db)

    def update_user(
        self,
        db: Session,
        user: UpdateUserModelSchema,
        id: int,
    ):
        user_in_db = db.query(UserModel).filter(UserModel.id == id).first()

        if user_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with given username not found",
            )

        update_data = user.dict(exclude_unset=True)

        try:
            for key, value in update_data.items():
                setattr(user_in_db, key, value)
            db.commit()
            db.refresh(user_in_db)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e,
            )

        return OutputUserModelSchema.from_orm(user_in_db)


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

        return OutputOrganizationModelSchema.from_orm(org_in_db)

    def fetch_organizations(
        self,
        db: Session,
    ):
        orgs_in_db = db.query(OrganizationModel).all()

        output_orgs_schemas = [
            OutputOrganizationModelSchema.from_orm(org) for org in orgs_in_db
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

        return OutputOrganizationModelSchema.from_orm(org_in_db)

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

        update_data = org.dict(exclude_unset=True)

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

        return OutputOrganizationModelSchema.from_orm(org_in_db)


class AddressRepo:
    def __init__(self) -> None:
        pass

    def create(
        self,
        db: Session,
        org_id: int,
        addr: AddressCreateSchema,
    ):
        addr_in_db = AddressModel()

        for key, value in addr:
            setattr(addr_in_db, key, value)

        setattr(addr_in_db, "organization_id", org_id)

        db.add(addr_in_db)
        db.commit()
        db.refresh(addr_in_db)

        return OutputAddressModelSchema.from_orm(addr_in_db)


class CustomFieldRepo:
    def __init__(self) -> None:
        pass

    def create(
        self,
        db: Session,
        org_id: int,
        custom_field: CustomFieldCreateSchema,
    ):
        custom_field_in_db = CustomFieldModel()

        for key, value in custom_field:
            setattr(custom_field_in_db, key, value)

        setattr(custom_field_in_db, "organization_id", org_id)

        db.add(custom_field_in_db)
        db.commit()
        db.refresh(custom_field_in_db)

        return OutputAddressModelSchema.from_orm(custom_field_in_db)
