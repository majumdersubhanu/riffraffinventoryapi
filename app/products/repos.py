from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.products.models import Product
from app.products.schemas import CreateProductSchema, OutputProductSchema


class ProductRepo:
    def __init__(self) -> None:
        pass

    def create_product(
        self,
        request_inventory: CreateProductSchema,
        db: Session,
    ):
        inventory_in_db = Product(
            warehouse_id=request_inventory.warehouse_id,
        )

        db.add(inventory_in_db)
        db.commit()
        db.refresh(inventory_in_db)

        if (
            db.query(Product)
            .filter(Product.warehouse_id == request_inventory.warehouse_id)
            .first()
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create product",
            )

        return OutputProductSchema.model_validate(inventory_in_db)

    def get_all_products(self, db: Session):
        inventories_in_db: List[Product] = db.query(Product).all()

        if len(inventories_in_db) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found",
            )

        return [
            OutputProductSchema.model_validate(inventory_in_db)
            for inventory_in_db in inventories_in_db
        ]

    def get_product(self, product_id: int, db: Session):
        inventory_in_db = db.query(Product).filter(Product.id == product_id).first()

        if inventory_in_db == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No product found",
            )

        return inventory_in_db
