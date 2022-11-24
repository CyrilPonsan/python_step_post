import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from dependancies.dependancies import get_db
from fixtures.fixtures import create_fixtures
from routing.auth_router import auth_router
from routing.client_router import client_router
from sql import models
from sql.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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

app.include_router(auth_router)
app.include_router(client_router)


class Settings(BaseModel):
    # to get a string like this run:
    # openssl rand -hex 32
    authjwt_secret_key: str = "3eb0244704381946964175c6613ed18e11ae37a737af82187409db74a0ccd380"
    authjwt_access_token_expires = 604800


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get("/fixtures")
def fixtures(db: Session = Depends(get_db)):
    return create_fixtures(db)


"""
if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
"""