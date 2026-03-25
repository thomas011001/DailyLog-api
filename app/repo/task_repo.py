from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from app.models import Task


class TaskRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: int) -> Task:
        stmt = select(Task).where(Task.id == task_id)
        return self.db.scalar(stmt)

    def create_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(
        self,
        task: Task,
        title: str | None = None,
        is_complete: bool | None = None,
    ) -> Task:
        if title is not None:
            task.title = title
        if is_complete is not None:
            task.is_complete = is_complete

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
