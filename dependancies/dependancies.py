from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from sql.database import SessionLocal


# Base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
