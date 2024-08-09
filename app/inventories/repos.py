from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.inventories.models import Inventory
from app.inventories.schemas import CreateInventorySchema, OutputInventorySchema


class InventoryRepo:
    def __init__(self) -> None:
        pass

    def create_inventory(
        self,
        request_inventory: CreateInventorySchema,
        db: Session,
    ):
        inventory_in_db = Inventory(
            shop_id=request_inventory.shop_id,
        )

        db.add(inventory_in_db)
        db.commit()
        db.refresh(inventory_in_db)

        if (
            db.query(Inventory)
            .filter(Inventory.shop_id == request_inventory.shop_id)
            .first()
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create inventory",
            )

        return OutputInventorySchema.model_validate(inventory_in_db)

    def get_all_inventories(self, db: Session):
        inventories_in_db: List[Inventory] = db.query(Inventory).all()

        if len(inventories_in_db) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No inventories found",
            )

        return [
            OutputInventorySchema.model_validate(inventory_in_db)
            for inventory_in_db in inventories_in_db
        ]
