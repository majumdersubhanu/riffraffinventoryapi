from fastapi import FastAPI
from app.base import Base
from app.database import engine
from app.organizations.routing.router import org_router
from app.users.routing.router import user_router
from app.shops.routing.router import shop_router
from app.inventory.routing.router import inventory_router
from app.products.routing.router import product_router
from app.warehouses.routing.router import warehouse_router

app = FastAPI(
    title="RiffRaff Inventory",
)

Base.metadata.create_all(
    bind=engine,
)

app.include_router(org_router)
app.include_router(user_router)
app.include_router(shop_router)
app.include_router(inventory_router)
app.include_router(warehouse_router)
app.include_router(product_router)
