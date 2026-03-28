from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_break_step_service, get_current_user
from app.exception import DayNotFoundError, ForbiddenDayAccessError, StepNotFoundError
from app.schemas import BreakStepCreate, BreakStepOut, BreakStepUpdate
from app.services.break_step_service import BreakStepService

break_step_router = APIRouter()


@break_step_router.post(
    "/days/{day_id}/break-steps",
    status_code=status.HTTP_201_CREATED,
    response_model=BreakStepOut,
)
def create_break_step(
    day_id: int,
    payload: BreakStepCreate,
    service: BreakStepService = Depends(get_break_step_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        return service.create_break_step(payload, current_user["id"], day_id)
    except DayNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@break_step_router.put(
    "/break-steps/{step_id}",
    status_code=status.HTTP_200_OK,
    response_model=BreakStepOut,
)
def edit_break_step(
    step_id: int,
    payload: BreakStepUpdate,
    service: BreakStepService = Depends(get_break_step_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        return service.edit_break_step(step_id, current_user["id"], payload)
    except StepNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Step not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )