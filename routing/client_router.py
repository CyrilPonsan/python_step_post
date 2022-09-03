from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dependancies.dependancies import get_db
from services import service_courrier
from sql import schemas, crud



client_router = APIRouter(prefix="/api")


@client_router.get("/courriers", response_model=list[schemas.ResponseCourrier])
async def courriers(filter: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    username = Authorize.get_jwt_subject()
    return await service_courrier.read_all_courriers(db, username, filter)

