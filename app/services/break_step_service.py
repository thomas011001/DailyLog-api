from sqlalchemy.exc import IntegrityError

from app.exception import DayNotFoundError, ForbiddenDayAccessError, StepNotFoundError
from app.models import BreakStep, Day
from app.repo.break_step_repo import BreakStepRepo
from app.repo.day_repo import DayRepo
from app.schemas import BreakStepCreate, BreakStepUpdate


class BreakStepService:
    def __init__(self, break_step_repo: BreakStepRepo, day_repo: DayRepo):
        self.break_step_repo = break_step_repo
        self.day_repo = day_repo

    def _get_day_or_404(self, day_id: int) -> Day:
        day = self.day_repo.get_day(day_id)
        if not day:
            raise DayNotFoundError()
        return day

    def _get_step_or_404(self, step_id: int) -> BreakStep:
        step = self.break_step_repo.get_break_step(step_id)
        if not step:
            raise StepNotFoundError()
        return step

    def _ensure_day_ownership(self, day: Day, user_id: int) -> None:
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def _ensure_step_ownership(self, step: BreakStep, user_id: int) -> None:
        day = step.day if step.day else self._get_day_or_404(step.day_id)
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def create_break_step(
        self, payload: BreakStepCreate, user_id: int, day_id: int
    ) -> BreakStep:
        day = self._get_day_or_404(day_id)
        self._ensure_day_ownership(day, user_id)

        new_step = BreakStep(day_id=day_id, **payload.model_dump())
        try:
            return self.break_step_repo.create_break_step(new_step)
        except IntegrityError as exc:
            raise DayNotFoundError() from exc

    def edit_break_step(
        self, step_id: int, user_id: int, payload: BreakStepUpdate
    ) -> BreakStep:
        step = self._get_step_or_404(step_id)
        self._ensure_step_ownership(step, user_id)
        return self.break_step_repo.update_break_step(
            step, description=payload.description
        )