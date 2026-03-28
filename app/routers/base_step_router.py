from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_base_step_service, get_current_user
from app.exception import DayNotFoundError, ForbiddenDayAccessError, StepNotFoundError
from app.schemas import StepOut
from app.services.base_step_service import BaseStepService

base_step_router = APIRouter()


@base_step_router.delete(
    "/steps/{step_id}",
    status_code=status.HTTP_200_OK,
)
def delete_step(
    step_id: int,
    service: BaseStepService = Depends(get_base_step_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        service.delete_step(step_id, current_user["id"])
        return {"detail": "Step deleted."}
    except StepNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Step not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@base_step_router.patch(
    "/steps/{step_id}/toggle",
    status_code=status.HTTP_200_OK,
    response_model=StepOut,
)
def toggle_step(
    step_id: int,
    service: BaseStepService = Depends(get_base_step_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        return service.toggle_step(step_id, current_user["id"])
    except StepNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Step not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )