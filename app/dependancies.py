import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repo.day_repo import DayRepo
from app.repo.user_repo import UserRepo

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserTokenData(BaseModel):
    id: int
    username: str


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            os.getenv("ACCESS_TOKEN_KEY", "very secret key"),
            algorithms=["HS256"],
        )
        username = payload["username"]
        id = payload["id"]
        return {"id": id, "username": username}
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate the current user.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_repo(db: Session = Depends(get_db)):
    return UserRepo(db)


def get_day_repo(db: Session = Depends(get_db)):
    return DayRepo(db)
