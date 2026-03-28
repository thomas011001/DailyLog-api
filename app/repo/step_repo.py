from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import BaseStep


class BaseStepRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_step(self, step_id: int) -> BaseStep | None:
        stmt = select(BaseStep).where(BaseStep.id == step_id)
        return self.db.scalar(stmt)

    def delete_step(self, step: BaseStep) -> BaseStep:
        self.db.delete(step)
        self.db.commit()
        return step

    def toggle_step(self, step: BaseStep) -> BaseStep:
        step.is_completed = not step.is_completed
        self.db.commit()
        self.db.refresh(step)
        return step