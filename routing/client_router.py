from fastapi import APIRouter, Depends, Form
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from dependancies.dependancies import get_db, get_Authorize
from services import service_courrier
from sql import schemas

client_router = APIRouter(prefix="/api")


class Settings(BaseModel):
    # to get a string like this run:
    # openssl rand -hex 32
    authjwt_secret_key: str = "3eb0244704381946964175c6613ed18e11ae37a737af82187409db74a0ccd380"


@AuthJWT.load_config
def get_config():
    return Settings()


@client_router.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@client_router.get("/user")
def read_token():
    return {"user": "current_user"}
