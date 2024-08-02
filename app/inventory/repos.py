from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.shops.models import Shop
from app.shops.schemas import CreateShopSchema, OutputShopSchema


class ShopRepo:
    def __init__(self) -> None:
        pass

    def create_shop(
        self,
        request_shop: CreateShopSchema,
        db: Session,
    ):
        shop_in_db = Shop(
            name=request_shop.name,
            vendor_id=request_shop.vendor_id,
        )

        db.add(shop_in_db)
        db.commit()
        db.refresh(shop_in_db)

        if db.query(Shop).filter(Shop.name == request_shop.name).first() is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create shop",
            )

        return OutputShopSchema.model_validate(shop_in_db)

    def get_all_shops(self, db: Session):
        shops_in_db: List[Shop] = db.query(Shop).all()

        if len(shops_in_db) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No shops found"
            )

        return [
            OutputShopSchema.model_validate(shop_in_db) for shop_in_db in shops_in_db
        ]
