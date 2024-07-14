from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class UserModel(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, index=True)
    organization = Column(String, index=True)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    isActive = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id} username={self.username} role={self.role} organization={self.organization} isActive={self.isActive})>"


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


class AddressModel(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    street_address1 = Column(String)
    street_address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    zip = Column(String)

    organization = relationship("OrganizationModel", back_populates="addresses")


class CustomFieldModel(Base):
    __tablename__ = "custom_fields"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    index = Column(Integer)
    value = Column(String)
    label = Column(String)

    organization = relationship("OrganizationModel", back_populates="custom_fields")
