from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from dependancies.dependancies import JWTBearer, get_db
from services import service_courrier
from sql import schemas

client_router = APIRouter(prefix="/api", dependencies=[Depends(JWTBearer())])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@client_router.post("/bordereau", response_model=schemas.ResponseBordereau)
async def read_bordereau(bordereau: str = Form(), db: Session = Depends(get_db)):
    return await service_courrier.read_bordereau(db, bordereau)


# la valeur True signifie qu'on veut en retour les courriers en cours de distribution
@client_router.get("/courriers", response_model=list[schemas.ResponseCourrier])
async def read_all_envois_en_cours(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return await service_courrier.read_all_courriers(db, token, True)


# la valeur False signifie qu'on veut en retour les courriers distribués ou retournés à l'expéditeur
@client_router.get("/historique", response_model=list[schemas.ResponseCourrier])
async def read_all_historique(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return await service_courrier.read_all_courriers(db, token, False)
