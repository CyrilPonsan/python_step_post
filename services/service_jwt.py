from datetime import datetime, timedelta
from typing import Any
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
import time

# to get a string like this run:
# openssl rand -hex 32
from sqlalchemy.orm import Session

from sql import crud

SECRET_KEY = "3eb0244704381946964175c6613ed18e11ae37a737af82187409db74a0ccd380"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240


def authenticate_user(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str) -> dict | None | dict[Any, Any]:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded_token["exp"] >= time.time():
            return decoded_token
        else:
            return None
    except:
        return {}


async def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    db_user = crud.get_user_by_email(db, form_data.username)
    if not authenticate_user(form_data.password, db_user.password):
        raise HTTPException(status_code=402, detail="Invalid credentials")
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}