from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.dependancies import get_current_user, get_day_repo
from app.models import Day
from app.repo.day_repo import DayRepo


class CreateDay(BaseModel):
    title: str | None = None
    date: date


class DayOut(BaseModel):
    id: int
    title: str | None = None
    date: date
    tasks: list[TaskOut]
    notes: list[NoteOut]


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: int = 1
    remind_at: datetime | None = None


class NoteOut(BaseModel):
    id: int
    content: str


class UpdateDay(BaseModel):
    title: str | None = None
    new_date: date | None = None


day_router = APIRouter()


@day_router.post("/day", response_model=DayOut, status_code=status.HTTP_201_CREATED)
def create_day(
    day: CreateDay,
    repo: DayRepo = Depends(get_day_repo),
    user: dict = Depends(get_current_user),
):
    try:
        new_day = Day(user_id=user["id"], title=day.title, date=day.date)
        return repo.create_day(new_day)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, "This Day Already Exist.")
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@day_router.delete("/day/{id}", status_code=status.HTTP_200_OK)
def delete_day(
    id: int,
    repo: DayRepo = Depends(get_day_repo),
    current_user: dict = Depends(get_current_user),
):

    try:
        day = repo.get_day(id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )

    if day.user_id != current_user["id"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")

    repo.delete_day(day)

    return {"detail": "Day deleted."}


@day_router.get("/day/{id}", status_code=status.HTTP_200_OK, response_model=DayOut)
def get_day_content(
    id: int,
    repo: DayRepo = Depends(get_day_repo),
    current_user: dict = Depends(get_current_user),
):
    try:
        day = repo.get_day_content(id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )

    if day.user_id != current_user["id"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")

    return day


@day_router.put("/day/{id}", status_code=status.HTTP_200_OK, response_model=DayOut)
def edit_day(
    id: int,
    day_update: UpdateDay,
    repo: DayRepo = Depends(get_day_repo),
    current_user: dict = Depends(get_current_user),
):
    try:
        day = repo.get_day(id)
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )

    if day.user_id != current_user["id"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")

    try:
        updated_day = repo.update_day(
            day, title=day_update.title, date=day_update.new_date
        )
        return updated_day
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, "This Day Already Exist.")
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


# edit a day name or date
