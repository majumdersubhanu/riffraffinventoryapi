from pydantic import BaseModel
from typing import Optional


class AddressBaseSchema(BaseModel):
    street_address1: Optional[str] = None
    street_address2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None

    class Config:
        from_attributes = True


class AddressCreateSchema(AddressBaseSchema):
    pass


class AddressUpdateSchema(AddressBaseSchema):
    id: int


class OutputAddressModelSchema(AddressBaseSchema):
    id: int