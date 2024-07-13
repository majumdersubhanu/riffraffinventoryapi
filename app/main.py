from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app import authentication as auth
from app.crud import UserRepo
import app.models as models
from app.db import engine, get_db
from app.schemas import (
    InputUserModelSchema,
    OutputUserModelSchema,
    UpdateUserModelSchema,
)
from datetime import timedelta
import jwt

app = FastAPI(title="RiffRaff Inventory")

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def root():
    return {"message": "Welcome to RiffRaff Inventory APIs"}


user_repo = UserRepo()


@app.post("/token")
async def generate_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = user_repo.login(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    authenticator = auth.Authenticator()
    tokens = authenticator.create_tokens(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": tokens["access"],
        "refresh_token": tokens["refresh"],
        "token_type": "bearer",
    }


# TODO: Typically we should perform a login right after the user has been created, i.e. return the JWT
@app.post("/users", response_model=OutputUserModelSchema, status_code=201)
def register_user(request_user: InputUserModelSchema, db: Session = Depends(get_db)):
    user = user_repo.create(db=db, user=request_user)
    return user


@app.get("/users/me/", response_model=OutputUserModelSchema)
async def fetch_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        authenticator = auth.Authenticator()
        payload = authenticator.decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User credential mismatch",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials | details={e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = user_repo.fetch_user_by_username(db=db, username=username)
    return user


@app.post("/token/refresh")
async def token_refresh(token: str, db: Session = Depends(get_db)):
    try:
        authenticator = auth.Authenticator()
        payload = authenticator.decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User credential mismatch",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials | details={e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = user_repo.fetch_user_by_username(db=db, username=username)
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    tokens = authenticator.create_tokens(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": tokens["access"],
        "refresh_token": token,
        "token_type": "bearer",
    }


@app.patch("/users/update/{id}", response_model=OutputUserModelSchema, status_code=200)
async def update_user_profile(
    id: int,
    request_user: UpdateUserModelSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    updated_user = user_repo.update_user(db=db, id=id, user=request_user)
    return updated_user
