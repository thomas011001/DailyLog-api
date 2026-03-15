from sqlalchemy.orm import Session, joinedload

from app.models import Note


class NoteRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_note(self, note_id: int) -> Note:
        note = (
            self.db.query(Note)
            .options(joinedload(Note.day))
            .filter(Note.id == note_id)
            .one()
        )
        return note

    def create_note(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update_note(self, note: Note, content: str | None = None) -> Note:
        if content is not None:
            note.content = content  # type: ignore
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete_note(self, note: Note) -> None:
        self.db.delete(note)
        self.db.commit()

