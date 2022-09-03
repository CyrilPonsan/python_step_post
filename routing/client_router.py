from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from dependancies.dependancies import get_db
from services import service_courrier
from sql import schemas

client_router = APIRouter(prefix="/api")


@client_router.get("/courriers", response_model=list[schemas.ResponseCourrier])
def courriers(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return service_courrier.read_all_courriers(db, user_id)


@client_router.get("/timeline", response_model=schemas.ResponseBordereau)
async def timeline(bordereau: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return await service_courrier.read_bordereau(db, bordereau, user_id)
