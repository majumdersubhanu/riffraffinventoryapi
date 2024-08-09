from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.shops.repos import ShopRepo
from app.shops.schemas import CreateShopSchema, OutputShopSchema

shop_router = APIRouter(
    tags=["Shops"],
    prefix="/shops",
)

shop_repo = ShopRepo()


@shop_router.post(
    path="/",
    status_code=201,
    response_model=OutputShopSchema,
)
def create_shop(
    request_shop: CreateShopSchema,
    db: Session = Depends(get_db),
) -> OutputShopSchema:
    output_shop = shop_repo.create_shop(
        db=db,
        request_shop=request_shop,
    )

    return output_shop


@shop_router.get(
    path="/",
    status_code=201,
    response_model=List[OutputShopSchema],
)
def get_all_shops(
    db: Session = Depends(get_db),
) -> List[OutputShopSchema]:
    output_shops = shop_repo.get_all_shops(
        db=db,
    )

    return output_shops
