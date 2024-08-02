from fastapi import FastAPI
from app.base import Base
from app.database import engine
from app.organizations.routing.router import org_router
from app.users.routing.router import user_router

app = FastAPI(
    title="RiffRaff Inventory",
)

Base.metadata.create_all(
    bind=engine,
)

app.include_router(org_router)
app.include_router(user_router)


@app.get(path="/", status_code=200)
def root():
    return {
        "message": "Welcome to RiffRaff Inventory",
    }
