import uvicorn
from fastapi import FastAPI, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import fixtures.fixtures
from dependancies.dependancies import get_db
from routing.client_router import client_router
from sql import models, schemas
from sql.database import engine
from services import service_user, service_jwt, service_courrier

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# liste des domaines autorisés
origins = [
    "http://localhost:4200",
    "http://localhost:40445"
]

# politique CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client_router)


# création d'un token valide
@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await service_jwt.login_for_access_token(form_data, db)


# interface admin pour la version dev
@app.get("/fixtures")
async def create_fixtures(db: Session = Depends(get_db)):
    return fixtures.fixtures.create_fixtures(db)


# création d'un nouvel utilisateur
@app.post("/user/new/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service_user.create_user(user, db)


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
