from pydantic import BaseModel
from typing import Optional


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