from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


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