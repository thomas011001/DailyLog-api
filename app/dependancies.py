import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi import status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.repo.break_step_repo import BreakStepRepo
from app.repo.day_repo import DayRepo
from app.repo.focus_session_repo import FocusSessionRepo
from app.repo.focus_step_repo import FocusStepRepo
from app.repo.step_repo import BaseStepRepo
from app.repo.user_repo import UserRepo
from app.repo.task_repo import TaskRepo
from app.services.base_step_service import BaseStepService
from app.services.break_step_service import BreakStepService
from app.services.day_service import DayService
from app.services.focus_session_service import FocusSessionService
from app.services.focus_step_service import FocusStepService
from app.services.task_service import TaskService

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


def get_task_repo(db: Session = Depends(get_db)):
    return TaskRepo(db)


def get_focus_step_repo(db: Session = Depends(get_db)):
    return FocusStepRepo(db)


def get_task_service(
    task_repo: TaskRepo = Depends(get_task_repo),
    day_repo: DayRepo = Depends(get_day_repo),
):
    return TaskService(task_repo=task_repo, day_repo=day_repo)


def get_focus_step_service(
    focus_step_repo: FocusStepRepo = Depends(get_focus_step_repo),
    day_repo: DayRepo = Depends(get_day_repo),
):
    return FocusStepService(focus_step_repo=focus_step_repo, day_repo=day_repo)


def get_day_service(day_repo: DayRepo = Depends(get_day_repo)):
    return DayService(day_repo)


def get_session_repo(db: Session = Depends(get_db)):
    return FocusSessionRepo(db)


def get_base_step_repo(db: Session = Depends(get_db)):
    return BaseStepRepo(db)


def get_session_sevice(
    day_repo: DayRepo = Depends(get_day_repo),
    session_repo: FocusSessionRepo = Depends(get_session_repo),
    base_step_repo: BaseStepRepo = Depends(get_base_step_repo),
):
    return FocusSessionService(session_repo, base_step_repo, day_repo)

def get_break_step_repo(db: Session = Depends(get_db)):
    return BreakStepRepo(db) 

def get_break_step_service(
    break_step_repo: BreakStepRepo = Depends(get_break_step_repo),
    day_repo: DayRepo = Depends(get_day_repo),
):
    return BreakStepService(break_step_repo=break_step_repo, day_repo=day_repo)

def get_base_step_service(
    base_step_repo: BaseStepRepo = Depends(get_base_step_repo),
    day_repo: DayRepo = Depends(get_day_repo),
):
    return BaseStepService(base_step_repo=base_step_repo, day_repo=day_repo)