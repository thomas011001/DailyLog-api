from sqlalchemy.exc import IntegrityError, NoResultFound

from app.exception import (
    DayNotFoundError,
    ForbiddenDayAccessError,
    TaskNotFoundError,
)
from app.models import Task
from app.repo.day_repo import DayRepo
from app.repo.task_repo import TaskRepo
from app.schemas import CreateTask, UpdateTask


class TaskService:
    def __init__(self, task_repo: TaskRepo, day_repo: DayRepo):
        self.task_repo = task_repo
        self.day_repo = day_repo

    def _ensure_day_ownership(self, day_id: int, user_id: int) -> None:
        try:
            day = self.day_repo.get_day(day_id)
        except NoResultFound as exc:
            raise DayNotFoundError() from exc

        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def _ensure_task_ownership(self, task: Task, user_id: int) -> None:
        if task.day is None:
            # Load day via repo to be safe
            day = self.day_repo.get_day(task.day_id)
        else:
            day = task.day
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def create_task(self, user_id: int, payload: CreateTask) -> Task:
        self._ensure_day_ownership(payload.day_id, user_id)
        task = Task(
            day_id=payload.day_id,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            remind_at=payload.remind_at,
            status=payload.status or "pending",
        )
        try:
            return self.task_repo.create_task(task)
        except IntegrityError as exc:
            # Likely due to FK or unique constraints
            raise DayNotFoundError() from exc

    def _get_task_or_404(self, task_id: int) -> Task:
        try:
            return self.task_repo.get_task(task_id)
        except NoResultFound as exc:
            raise TaskNotFoundError() from exc

    def edit_task(self, task_id: int, user_id: int, payload: UpdateTask) -> Task:
        task = self._get_task_or_404(task_id)
        self._ensure_task_ownership(task, user_id)

        # constrain status to either "pending" or "finished" if provided
        status_value = payload.status
        if status_value is not None and status_value not in {"pending", "finished"}:
            # Treat invalid status as no-op on status, or you could raise a dedicated error.
            status_value = None

        try:
            return self.task_repo.update_task(
                task,
                title=payload.title,
                description=payload.description,
                priority=payload.priority,
                remind_at=payload.remind_at,
                status=status_value,
            )
        except IntegrityError as exc:
            # In case of constraint issues, treat as not found / conflict
            raise TaskNotFoundError() from exc

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self._get_task_or_404(task_id)
        self._ensure_task_ownership(task, user_id)
        self.task_repo.delete_task(task)

