from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_current_user, get_note_service
from app.exception import DayNotFoundError, ForbiddenDayAccessError, NoteNotFoundError
from app.schemas import CreateNote, NoteOut, UpdateNote
from app.services.note_service import NoteService


note_router = APIRouter()


@note_router.post(
    "/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED
)
def create_note(
    payload: CreateNote,
    current_user: dict = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    try:
        note = service.create_note(user_id=current_user["id"], payload=payload)
        return note
    except DayNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@note_router.put(
    "/notes/{note_id}", response_model=NoteOut, status_code=status.HTTP_200_OK
)
def edit_note(
    note_id: int,
    payload: UpdateNote,
    current_user: dict = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    try:
        note = service.edit_note(
            note_id=note_id, user_id=current_user["id"], payload=payload
        )
        return note
    except NoteNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Note not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@note_router.delete("/notes/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(
    note_id: int,
    current_user: dict = Depends(get_current_user),
    service: NoteService = Depends(get_note_service),
):
    try:
        service.delete_note(note_id=note_id, user_id=current_user["id"])
    except NoteNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Note not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )

    return {"detail": "Note deleted."}

