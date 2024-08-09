from pydantic import BaseModel


class BaseInventorySchema(BaseModel):
    shop_id: int

    class Config:
        from_attributes = True


class CreateInventorySchema(BaseInventorySchema):
    pass


class OutputInventorySchema(BaseInventorySchema):
    id: int
