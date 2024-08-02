from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.shops.repos import ShopRepo
from app.shops.schemas import CreateShopSchema, OutputShopSchema

inventory_router = APIRouter(
    tags=["Inventory"],
    prefix="/inventories",
)

inventory_repo = ShopRepo()


@inventory_router.post(
    path="/",
    status_code=201,
    response_model=OutputShopSchema,
)
def create_organization(
    request_shop: CreateShopSchema,
    db: Session = Depends(get_db),
) -> OutputShopSchema:
    output_shop = inventory_repo.create_shop(
        db=db,
        request_shop=request_shop,
    )

    return output_shop


@inventory_router.get(
    path="/",
    status_code=201,
    response_model=List[OutputShopSchema],
)
def get_all_shops(
    db: Session = Depends(get_db),
) -> List[OutputShopSchema]:
    output_shops = inventory_repo.get_all_shops(
        db=db,
    )

    return output_shops
