from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.base import Base
from app.database import engine, get_db
from app.organization.models import Organization
from app.organization.schemas import CreateOrganizationSchema, OutputOrganizationSchema
from app.users.models import User
from app.users.schemas import CreateUserSchema, OutputUserSchema

app = FastAPI(
    title="RiffRaff Inventory",
)

Base.metadata.create_all(
    bind=engine,
)


@app.get(path="/", status_code=200)
def root():
    return {
        "message": "Welcome to RiffRaff Inventory",
    }


@app.get(path="/users", status_code=200)
def get_users(db: Session = Depends(get_db)):
    db.query(User).all()


@app.post(path="/users", status_code=201)
def create_user(request_user: CreateUserSchema, db: Session = Depends(get_db)):
    user_in_db = User(
        username=request_user.username,
        password=request_user.password,
        f_name=request_user.f_name,
        l_name=request_user.l_name,
        email=request_user.email,
        role=request_user.role,
    )

    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)

    if db.query(User).filter(User.username == request_user.username).first() is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user",
        )

    return OutputUserSchema.model_validate(user_in_db)


@app.get(path="/organizations", status_code=200)
def get_organizations(db: Session = Depends(get_db)):
    db.query(Organization).all()


@app.post(path="/organizations", status_code=201)
def create_organization(
    request_org: CreateOrganizationSchema, db: Session = Depends(get_db)
):
    org_in_db = Organization(
        name=request_org.name,
        admin_id=request_org.admin_id,
    )

    db.add(org_in_db)
    db.commit()
    db.refresh(org_in_db)

    if (
        db.query(Organization).filter(Organization.name == request_org.name).first()
        is None
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create organization",
        )

    return OutputOrganizationSchema.model_validate(org_in_db)
