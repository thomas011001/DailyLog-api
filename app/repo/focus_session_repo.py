from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import FocusSession


class FocusSessionRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_focus_session(self, focus_session: FocusSession):
        self.db.add(focus_session)
        self.db.commit()
        self.db.refresh(focus_session)
        return focus_session

    def delete_focus_session(self, focus_session: FocusSession):
        self.db.delete(focus_session)
        self.db.commit()
        return focus_session
    
    def toggle_focus_session(self, focus_session: FocusSession):
        focus_session.is_completed = not focus_session.is_completed

        self.db.commit()
        self.db.refresh(focus_session)

        return focus_session
    
    def get_focus_session(self, focus_session_id: int):
        stmt = select(FocusSession).where(FocusSession.id == focus_session_id)
        return self.db.scalar(stmt)