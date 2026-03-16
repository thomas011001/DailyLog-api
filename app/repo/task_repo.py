from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from app.models import Task


class TaskRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_task(self, task_id: int) -> Task:
        task = (
            self.db.query(Task)
            .options(joinedload(Task.day))
            .filter(Task.id == task_id)
            .one()
        )
        return task

    def create_task(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_task(
        self,
        task: Task,
        title: str | None = None,
        description: str | None = None,
        priority: int | None = None,
        remind_at=None,
        status: str | None = None,
    ) -> Task:
        if title is not None:
            task.title = title  # type: ignore
        if description is not None:
            task.description = description  # type: ignore
        if priority is not None:
            task.priority = priority  # type: ignore
        if remind_at is not None:
            task.remind_at = remind_at  # type: ignore
        if status is not None:
            task.status = status  # type: ignore

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

