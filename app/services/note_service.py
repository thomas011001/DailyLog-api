from sqlalchemy.exc import IntegrityError, NoResultFound

from app.exception import (
    DayNotFoundError,
    ForbiddenDayAccessError,
    NoteNotFoundError,
)
from app.models import Note
from app.repo.day_repo import DayRepo
from app.repo.note_repo import NoteRepo
from app.schemas import CreateNote, UpdateNote


class NoteService:
    def __init__(self, note_repo: NoteRepo, day_repo: DayRepo):
        self.note_repo = note_repo
        self.day_repo = day_repo

    def _ensure_day_ownership(self, day_id: int, user_id: int) -> None:
        try:
            day = self.day_repo.get_day(day_id)
        except NoResultFound as exc:
            raise DayNotFoundError() from exc

        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def _ensure_note_ownership(self, note: Note, user_id: int) -> None:
        if note.day is None:
            day = self.day_repo.get_day(note.day_id)
        else:
            day = note.day
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def create_note(self, user_id: int, payload: CreateNote) -> Note:
        self._ensure_day_ownership(payload.day_id, user_id)
        note = Note(day_id=payload.day_id, content=payload.content)
        try:
            return self.note_repo.create_note(note)
        except IntegrityError as exc:
            raise DayNotFoundError() from exc

    def _get_note_or_404(self, note_id: int) -> Note:
        try:
            return self.note_repo.get_note(note_id)
        except NoResultFound as exc:
            raise NoteNotFoundError() from exc

    def edit_note(self, note_id: int, user_id: int, payload: UpdateNote) -> Note:
        note = self._get_note_or_404(note_id)
        self._ensure_note_ownership(note, user_id)
        try:
            return self.note_repo.update_note(note, content=payload.content)
        except IntegrityError as exc:
            raise NoteNotFoundError() from exc

    def delete_note(self, note_id: int, user_id: int) -> None:
        note = self._get_note_or_404(note_id)
        self._ensure_note_ownership(note, user_id)
        self.note_repo.delete_note(note)
