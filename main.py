import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from sql import models, schemas, crud
from sql.database import engine
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def authenticate_user(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


class Settings(BaseModel):
    # to get a string like this run:
    # openssl rand -hex 32
    authjwt_secret_key: str = "3eb0244704381946964175c6613ed18e11ae37a737af82187409db74a0ccd380"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.post("/login")
def login(user: schemas.UserCreate, Authorize: AuthJWT = Depends(), db: Session = Depends()):
    db_user = crud.get_user_by_email(db, user.username)
    if user:
        if not authenticate_user(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Identifiants incorrects")
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}


@app.get("/user")
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
