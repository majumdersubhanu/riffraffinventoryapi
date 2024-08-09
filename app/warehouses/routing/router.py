from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.warehouses.repos import WarehouseRepo
from app.warehouses.schemas import CreateWarehouseSchema, OutputWarehouseSchema

warehouse_router = APIRouter(
    tags=["Warehouses"],
    prefix="/warehouses",
)

warehouse_repo = WarehouseRepo()


@warehouse_router.post(
    path="/",
    status_code=201,
    response_model=OutputWarehouseSchema,
)
def create_warehouse(
    request_warehouse: CreateWarehouseSchema,
    db: Session = Depends(get_db),
) -> OutputWarehouseSchema:
    inventory_shop = warehouse_repo.create_warehouse(
        db=db,
        request_warehouse=request_warehouse,
    )

    return inventory_shop


@warehouse_router.get(
    path="/",
    status_code=201,
    response_model=List[OutputWarehouseSchema],
)
def get_all_warehouses(
    db: Session = Depends(get_db),
) -> List[OutputWarehouseSchema]:
    output_inventories = warehouse_repo.get_all_warehouses(
        db=db,
    )

    return output_inventories
