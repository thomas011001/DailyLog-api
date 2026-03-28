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
<<<<<<< HEAD
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
=======
        is_complete: bool | None = None,
    ) -> Task:
        if title is not None:
            task.title = title
        if is_complete is not None:
            task.is_complete = is_complete
>>>>>>> dev

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
