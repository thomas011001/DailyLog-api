from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models import BaseStep, FocusSession, FocusStep


class FocusStepRepo:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_focus_step(self, focus_step: FocusStep):
        last_order = (
            self.db.query(func.max(BaseStep.order))
            .filter(BaseStep.day_id == focus_step.day_id)
            .scalar()
            or 0
        )
        new_order = last_order + 1
        focus_step.order = new_order
        for _ in range(focus_step.sessions_count):
            focus_step.sessions.append(FocusSession())
        self.db.add(focus_step)
        self.db.commit()
        stmt = (
            select(FocusStep)
            .options(joinedload(FocusStep.sessions))
            .where(FocusStep.id == focus_step.id)
        )
        return self.db.execute(stmt).unique().scalar_one()
