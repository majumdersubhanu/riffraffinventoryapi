from pydantic import BaseModel


class BaseWarehouseSchema(BaseModel):
    inventory_id: int

    class Config:
        from_attributes = True


class CreateWarehouseSchema(BaseWarehouseSchema):
    pass


class OutputWarehouseSchema(BaseWarehouseSchema):
    id: int
