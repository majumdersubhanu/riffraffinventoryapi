from pydantic import BaseModel


class BaseShopSchema(BaseModel):
    name: str
    vendor_id: int

    class Config:
        from_attributes = True


class CreateShopSchema(BaseShopSchema):
    pass


class OutputShopSchema(BaseShopSchema):
    id: int
