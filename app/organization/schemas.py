from pydantic import BaseModel


class BaseOrganizationSchema(BaseModel):
    name: str
    admin_id: int

    class Config:
        from_attributes = True


class CreateOrganizationSchema(BaseOrganizationSchema):
    pass


class OutputOrganizationSchema(BaseOrganizationSchema):
    id: int
