from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import tzlocal

from addresses.schemas import AddressBaseSchema
from app.schemas import CustomFieldBaseSchema


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
