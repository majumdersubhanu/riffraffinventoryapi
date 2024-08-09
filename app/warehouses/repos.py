from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.warehouses.models import Warehouse
from app.warehouses.schemas import CreateWarehouseSchema, OutputWarehouseSchema


class WarehouseRepo:
    def __init__(self) -> None:
        pass

    def create_warehouse(
        self,
        request_warehouse: CreateWarehouseSchema,
        db: Session,
    ):
        warehouse_in_db = Warehouse(
            inventory_id=request_warehouse.inventory_id,
        )

        db.add(warehouse_in_db)
        db.commit()
        db.refresh(warehouse_in_db)

        if (
            db.query(Warehouse)
            .filter(Warehouse.inventory_id == request_warehouse.inventory_id)
            .first()
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create warehouse",
            )

        return OutputWarehouseSchema.model_validate(warehouse_in_db)

    def get_all_warehouses(self, db: Session):
        warehouses_in_db: List[Warehouse] = db.query(Warehouse).all()

        if len(warehouses_in_db) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No warehouses found",
            )

        return [
            OutputWarehouseSchema.model_validate(warehouse_in_db)
            for warehouse_in_db in warehouses_in_db
        ]
