from jose import jwt, JWTError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from services.service_jwt import SECRET_KEY, ALGORITHM
from sql.schemas import TokenData
from sql import schemas, crud


def create_user(user: schemas.UserCreate, db: Session):
    db_user = crud.get_user_by_email(db, user.username)
    if not db_user:
        db_user = crud.create_user(db, user)
        return db_user
    raise HTTPException(status_code=400, detail="Email not available")


async def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception


async def read_current_user(db: Session, token: str):
    token_data = await get_current_user(token)
    db_user = crud.get_user_by_email(db, token_data.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
