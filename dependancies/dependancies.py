from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse

from main import app
from sql.database import SessionLocal





def get_Authorize(Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
    finally:
        next()


# Base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
