from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class CustomFieldModel(Base):
    __tablename__ = "custom_fields"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    index = Column(Integer)
    value = Column(String)
    label = Column(String)

    organization = relationship("OrganizationModel", back_populates="custom_fields")