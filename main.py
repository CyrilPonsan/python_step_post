import uvicorn
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from routing.client_router import client_router
from sql import models, schemas
from sql.database import engine
from services import service_user, service_jwt, service_courrier
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse

from sql.models import User

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(client_router)

class User(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != "toto@toto.fr":
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
