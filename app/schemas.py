from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import tzlocal


class BaseUserModelSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str] = "admin"
    organization: Optional[str] = None
    isActive: bool | None = False

    class Config:
        from_attributes = True


class InputUserModelSchema(BaseUserModelSchema):
    password: str


class InDBUserModelSchema(BaseUserModelSchema):
    id: int
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class OutputUserModelSchema(BaseUserModelSchema):
    id: int
    createdAt: Optional[datetime]


class UpdateUserModelSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None
    isActive: Optional[bool] = None
    password: Optional[str] = None
    updatedAt: Optional[datetime] = None


# Address Schemas
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


# Custom Field Schemas
class CustomFieldBaseSchema(BaseModel):
    index: Optional[int] = None
    value: Optional[str] = None
    label: Optional[str] = None

    class Config:
        from_attributes = True


class CustomFieldCreateSchema(CustomFieldBaseSchema):
    pass


class CustomFieldUpdateSchema(CustomFieldBaseSchema):
    id: int


class OutputCustomFieldModelSchema(CustomFieldBaseSchema):
    id: int


# Organization Schemas
class OrganizationBaseSchema(BaseModel):
    name: Optional[str] = None
    fiscal_year_start_month: Optional[str] = "Apr"
    currency_code: Optional[str] = "INR"
    time_zone: Optional[str] = tzlocal.get_localzone_name()
    date_format: Optional[str] = "ISO8601"  # Short Date, Long Date
    field_separator: Optional[str] = "-"
    language_code: Optional[str] = "En-In"
    industry_type: Optional[str] = None
    industry_size: Optional[str] = None
    portal_name: Optional[str] = None
    org_address: Optional[str] = None
    remit_to_address: Optional[str] = None
    is_default_org: Optional[bool] = True
    account_created_date: Optional[datetime] = datetime.now()
    contact_name: Optional[str] = None
    company_id_label: Optional[str] = None
    company_id_value: Optional[str] = None
    tax_id_label: Optional[str] = None
    tax_id_value: Optional[str] = None
    currency_id: Optional[str] = "INR"
    currency_symbol: Optional[str] = "Rs"
    currency_format: Optional[str] = None
    price_precision: Optional[int] = 2
    phone: Optional[str] = None
    fax: Optional[str] = None
    website: Optional[str] = None
    email: Optional[EmailStr] = None
    is_org_active: Optional[bool] = True
    addresses: Optional[List[AddressBaseSchema]] = []
    custom_fields: Optional[List[CustomFieldBaseSchema]] = []

    class Config:
        from_attributes = True


class OrganizationCreateSchema(OrganizationBaseSchema):
    pass


class OrganizationUpdateSchema(OrganizationBaseSchema):
    pass


class OutputOrganizationModelSchema(OrganizationBaseSchema):
    id: int
