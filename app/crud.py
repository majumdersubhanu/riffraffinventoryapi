from sqlalchemy.orm import Session

from app.models import CustomFieldModel
from app.schemas import CustomFieldCreateSchema, OutputCustomFieldModelSchema

from app.addresses.schemas import OutputAddressModelSchema


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

        return OutputCustomFieldModelSchema.model_validate(custom_field_in_db)
