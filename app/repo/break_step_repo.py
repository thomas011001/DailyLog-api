from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import BaseStep, BreakStep

_UNSET = object()


class BreakStepRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_break_step(self, break_step: BreakStep) -> BreakStep:
        last_order = (
            self.db.query(func.max(BaseStep.order))
            .filter(BaseStep.day_id == break_step.day_id)
            .scalar()
            or 0
        )
        break_step.order = last_order + 1
        self.db.add(break_step)
        self.db.commit()
        self.db.refresh(break_step)
        return break_step

    def update_break_step(self, break_step: BreakStep, description=_UNSET) -> BreakStep:
        if description is not _UNSET:
            break_step.description = description # type: ignore
        self.db.commit()
        self.db.refresh(break_step)
        return break_step

    def get_break_step(self, step_id: int) -> BreakStep | None:
        stmt = select(BreakStep).where(BreakStep.id == step_id)
        return self.db.scalar(stmt)