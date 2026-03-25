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