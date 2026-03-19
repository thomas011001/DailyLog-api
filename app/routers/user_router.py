from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_current_user, get_user_repo
from app.repo.user_repo import UserRepo
from app.schemas import DayOut
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.get(
    "/me/days", status_code=status.HTTP_200_OK, response_model=list[DayOut]
)
def get_current_user_days(
    user: dict = Depends(get_current_user), repo: UserRepo = Depends(get_user_repo)
):
    service = UserService(repo)
    try:
        days = service.get_user_days(user["id"])
        return days
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )
