from pydantic import BaseModel


class BaseProductSchema(BaseModel):
    warehouse_id: int

    class Config:
        from_attributes = True


class CreateProductSchema(BaseProductSchema):
    pass


class OutputProductSchema(BaseProductSchema):
    id: int
