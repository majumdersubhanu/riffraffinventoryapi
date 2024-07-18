from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from app.db import Base


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fiscal_year_start_month = Column(String)
    currency_code = Column(String)
    time_zone = Column(String)
    date_format = Column(String)
    field_separator = Column(String)
    language_code = Column(String)
    industry_type = Column(String)
    industry_size = Column(String)
    portal_name = Column(String)
    org_address = Column(String)
    remit_to_address = Column(String)
    is_default_org = Column(Boolean, default=False)
    account_created_date = Column(DateTime, default=func.now())
    contact_name = Column(String)
    company_id_label = Column(String)
    company_id_value = Column(String)
    tax_id_label = Column(String)
    tax_id_value = Column(String)
    currency_id = Column(String)
    currency_symbol = Column(String)
    currency_format = Column(String)
    price_precision = Column(Integer)
    phone = Column(String)
    fax = Column(String)
    website = Column(String)
    email = Column(String)
    is_org_active = Column(Boolean, default=True)

    addresses = relationship("AddressModel", back_populates="organization")
    custom_fields = relationship("CustomFieldModel", back_populates="organization")
