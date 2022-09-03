from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from sql.database import SessionLocal


# Base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_Authorize(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()