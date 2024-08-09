from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.inventories.repos import InventoryRepo
from app.inventories.schemas import CreateInventorySchema, OutputInventorySchema

inventory_router = APIRouter(
    tags=["Inventories"],
    prefix="/inventories",
)

inventory_repo = InventoryRepo()


@inventory_router.post(
    path="/",
    status_code=201,
    response_model=OutputInventorySchema,
)
def create_inventory(
    request_inventory: CreateInventorySchema,
    db: Session = Depends(get_db),
) -> OutputInventorySchema:
    inventory_shop = inventory_repo.create_inventory(
        db=db,
        request_inventory=request_inventory,
    )

    return inventory_shop


@inventory_router.get(
    path="/",
    status_code=201,
    response_model=List[OutputInventorySchema],
)
def get_all_inventories(
    db: Session = Depends(get_db),
) -> List[OutputInventorySchema]:
    output_inventories = inventory_repo.get_all_inventories(
        db=db,
    )

    return output_inventories
