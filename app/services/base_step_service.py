from sqlalchemy.exc import IntegrityError

from app.exception import DayNotFoundError, ForbiddenDayAccessError, StepNotFoundError
from app.models import BaseStep
from app.repo.day_repo import DayRepo
from app.repo.step_repo import BaseStepRepo


class BaseStepService:
    def __init__(self, base_step_repo: BaseStepRepo, day_repo: DayRepo):
        self.base_step_repo = base_step_repo
        self.day_repo = day_repo

    def _get_step_or_404(self, step_id: int) -> BaseStep:
        step = self.base_step_repo.get_step(step_id)
        if not step:
            raise StepNotFoundError()
        return step

    def _ensure_step_ownership(self, step: BaseStep, user_id: int) -> None:
        day = step.day if step.day else self.day_repo.get_day(step.day_id)
        if not day:
            raise DayNotFoundError()
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def delete_step(self, step_id: int, user_id: int) -> BaseStep:
        step = self._get_step_or_404(step_id)
        self._ensure_step_ownership(step, user_id)
        return self.base_step_repo.delete_step(step)

    def toggle_step(self, step_id: int, user_id: int) -> BaseStep:
        step = self._get_step_or_404(step_id)
        self._ensure_step_ownership(step, user_id)
        return self.base_step_repo.toggle_step(step)