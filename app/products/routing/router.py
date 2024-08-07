from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.products.repos import ProductRepo
from app.products.schemas import CreateProductSchema, OutputProductSchema

product_router = APIRouter(
    tags=["Products"],
    prefix="/products",
)

product_repo = ProductRepo()


@product_router.post(
    path="/",
    status_code=201,
    response_model=OutputProductSchema,
)
def create_product(
    request_inventory: CreateProductSchema,
    db: Session = Depends(get_db),
) -> OutputProductSchema:
    inventory_shop = product_repo.create_product(
        db=db,
        request_inventory=request_inventory,
    )

    return inventory_shop


@product_router.get(
    path="/",
    status_code=201,
    response_model=List[OutputProductSchema],
)
def get_all_products(
    db: Session = Depends(get_db),
) -> List[OutputProductSchema]:
    output_inventories = product_repo.get_all_products(
        db=db,
    )

    return output_inventories


@product_router.get(
    path="/{id}/",
    status_code=201,
    response_model=OutputProductSchema,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> OutputProductSchema:
    output_inventories = product_repo.get_product(
        db=db,
        product_id=product_id,
    )

    return OutputProductSchema.model_validate(output_inventories)
