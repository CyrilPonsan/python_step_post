import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import fixtures.fixtures
from dependancies.dependancies import JWTBearer, get_db
from sql import models, schemas
from sql.database import engine
from services import service_user, service_jwt, service_courrier

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()
# app.include_router(toto_route, prefix="/toto", dependencies=[Depends(JWTBearer())])

# liste des domaines autorisés
origins = [
    "http://localhost:4200",
]

# politique CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/courriers", dependencies=[Depends(JWTBearer())], response_model=list[schemas.EnvoiEnCours])
async def read_all_envois_en_cours(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return await service_courrier.read_all_courriers(db, token, True)


@app.get("/fixtures")
async def create_fixtures(db: Session = Depends(get_db)):
    return fixtures.fixtures.create_fixtures(db)


@app.get("/historique", dependencies=[Depends(JWTBearer)], response_model=list[schemas.EnvoiEnCours])
async def read_all_historique(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return await service_courrier.read_all_courriers(db, token, False)


@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await service_jwt.login_for_access_token(form_data, db)


@app.get("/users/me", response_model=schemas.User)
async def read_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return await service_user.read_current_user(db, token)


# interface admin pour la version dev
@app.post("/user/new/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service_user.create_user(user, db)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
