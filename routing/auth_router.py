from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from dependancies.dependancies import get_db
from sql import schemas, crud

auth_router = APIRouter(prefix="/auth")


def authenticate_user(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


@auth_router.post("/login")
def login(user: schemas.UserCreate, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.username)
    if user:
        if not authenticate_user(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Identifiants incorrects")
    access_token = Authorize.create_access_token(subject=db_user.id)
    return {"access_token": access_token}


@auth_router.get("/user")
def user(Authorize: AuthJWT = Depends()):
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}