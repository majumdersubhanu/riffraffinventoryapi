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

        user_in_db = UserModel(
            username=user.username,
            email=user.email,
            password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            organization=user.organization,
        )
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
        org_in_db = OrganizationModel(
            name=org.name,
            fiscal_year_start_month=org.fiscal_year_start_month,
            currency_code=org.currency_code,
            time_zone=org.time_zone,
            date_format=org.date_format,
            field_separator=org.field_separator,
            language_code=org.language_code,
            industry_type=org.industry_type,
            industry_size=org.industry_size,
            portal_name=org.portal_name,
            org_address=org.org_address,
            remit_to_address=org.remit_to_address,
            is_default_org=org.is_default_org,
            account_created_date=org.account_created_date,
            contact_name=org.contact_name,
            company_id_label=org.company_id_label,
            company_id_value=org.company_id_value,
            tax_id_label=org.tax_id_label,
            tax_id_value=org.tax_id_value,
            currency_id=org.currency_id,
            currency_symbol=org.currency_symbol,
            currency_format=org.currency_format,
            price_precision=org.price_precision,
            phone=org.phone,
            fax=org.fax,
            website=org.website,
            email=org.email,
            is_org_active=org.is_org_active,
        )

        db.add(org_in_db)
        db.commit()
        db.refresh(org_in_db)

        # Adding addresses if any
        if org.addresses is not None:
            for addr in org.addresses:
                db_addr = AddressModel(
                    organization_id=org_in_db.id,
                    street_address1=addr.street_address1,
                    street_address2=addr.street_address2,
                    city=addr.city,
                    state=addr.state,
                    country=addr.country,
                    zip=addr.zip,
                )
                db.add(db_addr)
                db.commit()
                db.refresh(db_addr)

        # Adding custom fields if any
        if org.custom_fields is not None:
            for custom_field in org.custom_fields:
                db_custom_field = CustomFieldModel(
                    organization_id=org_in_db.id,
                    index=custom_field.index,
                    value=custom_field.value,
                    label=custom_field.label,
                )
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

    def update_organization(
        self,
        db: Session,
        id: int,
        org: OrganizationUpdateSchema,
    ):
        org_in_db = (
            db.query(OrganizationModel).filter(OrganizationModel.id == id).first()
        )

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
        addr_in_db = AddressModel(
            organization_id=org_id,
            street_address1=addr.street_address1,
            street_address2=addr.street_address2,
            city=addr.city,
            state=addr.state,
            country=addr.country,
            zip=addr.zip,
        )

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
        index: int,
    ):
        custom_field_in_db = CustomFieldModel(
            organization_id=org_id,
            index=custom_field.index,
            label=custom_field.label,
            value=custom_field.value,
        )

        db.add(custom_field_in_db)
        db.commit()
        db.refresh(custom_field_in_db)

        return OutputAddressModelSchema.from_orm(custom_field_in_db)
