from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_current_user, get_session_sevice
from app.exception import (
    DayNotFoundError,
    ForbiddenDayAccessError,
    SessionNotFoundError,
    StepNotFoundError,
)
from app.schemas import FocusSessionOut
from app.services.focus_session_service import FocusSessionService


focus_session_router = APIRouter()


@focus_session_router.post(
    "/focus_steps/{step_id}/sessions",
    status_code=status.HTTP_201_CREATED,
    response_model=FocusSessionOut,
)
def create_focus_session(
    step_id: int,
    current_user: dict = Depends(get_current_user),
    service: FocusSessionService = Depends(get_session_sevice),
):
    try:
        return service.create_session(step_id, current_user["id"])
    except StepNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Step not found.")
    except DayNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@focus_session_router.delete(
    "/sessions/{session_id}",
    status_code=status.HTTP_200_OK,
)
def delete_focus_session(
    session_id: int,
    current_user: dict = Depends(get_current_user),
    service: FocusSessionService = Depends(get_session_sevice),
):
    try:
        service.delete_session(session_id, current_user["id"])
        return {"detail": "Session deleted."}
    except SessionNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@focus_session_router.patch(
    "/sessions/{session_id}/toggle",
    status_code=status.HTTP_200_OK,
    response_model=FocusSessionOut,
)
def toggle_focus_session(
    session_id: int,
    current_user: dict = Depends(get_current_user),
    service: FocusSessionService = Depends(get_session_sevice),
):
    try:
        return service.toggle_session(session_id, current_user["id"])
    except SessionNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )