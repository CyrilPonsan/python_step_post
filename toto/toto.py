from fastapi import APIRouter

toto_route = APIRouter()


@toto_route.get("/")
async def get_toto():
    return {"message": "toto"}