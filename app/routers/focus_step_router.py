from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_current_user, get_focus_step_service
from app.exception import DayNotFoundError, ForbiddenDayAccessError
from app.schemas import FocusStepCreate, FocusStepOut
from app.services.focus_step_service import FocusStepService

focus_step_router = APIRouter()


@focus_step_router.post(
    "/days/{id}/focus-steps",
    status_code=status.HTTP_201_CREATED,
    response_model=FocusStepOut,
)
def create_focus_steps(
    id: int,
    focus_step: FocusStepCreate,
    service: FocusStepService = Depends(get_focus_step_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        return service.create_focus_step(focus_step, current_user["id"], id)
    except DayNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )
