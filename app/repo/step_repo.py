from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import BaseStep


class BaseStepRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_step(self, step_id: int):
        stmt = select(BaseStep).where(BaseStep.id == step_id)
        return self.db.scalar(stmt)
