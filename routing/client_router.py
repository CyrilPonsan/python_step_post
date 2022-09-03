from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

client_router = APIRouter(prefix="/api")


@client_router.get("/user")
def read_token():
    return {"user": "current_user"}
