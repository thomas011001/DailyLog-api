from sqlalchemy.exc import IntegrityError, NoResultFound

from app.exception import (
    DayNotFoundError,
    ForbiddenDayAccessError,
    TaskNotFoundError,
)
from app.models import Day, Task
from app.repo.day_repo import DayRepo
from app.repo.task_repo import TaskRepo
from app.schemas import CreateTask, UpdateTask


class TaskService:
    def __init__(self, task_repo: TaskRepo, day_repo: DayRepo):
        self.task_repo = task_repo
        self.day_repo = day_repo

    def _ensure_day_ownership(self, day: Day, user_id: int) -> None:
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def _ensure_task_ownership(self, task: Task, user_id: int) -> None:
        if task.day is None:
            # Load day via repo to be safe
            day = self.day_repo.get_day(task.day_id)
            if not day:
                raise DayNotFoundError()
        else:
            day = task.day
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()


    def _get_task_or_404(self, task_id: int) -> Task:
        task = self.task_repo.get_task(task_id)
        if not task:
            raise TaskNotFoundError()
        return task

    def create_task(self, user_id: int, payload: CreateTask, day_id: int) -> Task:

        day = self.day_repo.get_day(day_id)
        if not day:
            raise DayNotFoundError()

        self._ensure_day_ownership(day, user_id)

        task = Task(**payload.model_dump(), day_id=day_id)
        try:
            return self.task_repo.create_task(task)
        except IntegrityError as exc:
            # Likely due to FK or unique constraints
            raise DayNotFoundError() from exc

    def edit_task(self, task_id: int, user_id: int, payload: UpdateTask) -> Task:
        task = self._get_task_or_404(task_id)
        self._ensure_task_ownership(task, user_id)

        try:
            return self.task_repo.update_task(task, **payload.model_dump())
        except IntegrityError as exc:
            # In case of constraint issues, treat as not found / conflict
            raise TaskNotFoundError() from exc

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self._get_task_or_404(task_id)
        self._ensure_task_ownership(task, user_id)
        self.task_repo.delete_task(task)
