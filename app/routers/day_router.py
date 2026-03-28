from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_current_user, get_day_repo, get_day_service
from app.exception import DayConflictError, DayNotFoundError, ForbiddenDayAccessError
from app.repo.day_repo import DayRepo
from app.schemas import CreateDay, DayOut, UpdateDay
from app.services.day_service import DayService

day_router = APIRouter()


@day_router.post("/day", response_model=DayOut, status_code=status.HTTP_201_CREATED)
def create_day(
    day: CreateDay,
    service: DayService = Depends(get_day_service),
    user: dict = Depends(get_current_user),
):
    try:
        new_day = service.create_day(user_id=user["id"], payload=day)
        return new_day
    except DayConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT, "This Day Already Exist.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@day_router.delete("/day/{id}", status_code=status.HTTP_200_OK)
def delete_day(
    id: int,
    service: DayService = Depends(get_day_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        return service.delete_day(day_id=id, user_id=current_user["id"])
    except DayNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@day_router.get("/day/{id}", status_code=status.HTTP_200_OK, response_model=DayOut)
def get_day_content(
    id: int,
    service: DayService = Depends(get_day_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        day = service.get_day_content(day_id=id, user_id=current_user["id"])
    except DayNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )

    return day


@day_router.put("/day/{id}", status_code=status.HTTP_200_OK, response_model=DayOut)
def edit_day(
    id: int,
    day_update: UpdateDay,
    service: DayService = Depends(get_day_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        updated_day = service.edit_day(
            day_id=id, user_id=current_user["id"], payload=day_update
        )
        return updated_day
    except DayNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except DayConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT, "This Day Already Exist.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )
