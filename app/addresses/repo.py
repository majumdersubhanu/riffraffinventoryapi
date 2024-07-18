from sqlalchemy.orm import Session

from app.addresses.models import AddressModel
from app.addresses.schemas import (
    AddressCreateSchema,
    OutputAddressModelSchema,
)


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

        return OutputAddressModelSchema.model_validate(addr_in_db)