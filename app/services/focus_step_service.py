from sqlalchemy.exc import IntegrityError

from app.exception import DayNotFoundError, ForbiddenDayAccessError
from app.models import BaseStep, Day, FocusStep
from app.repo.day_repo import DayRepo
from app.repo.focus_step_repo import FocusStepRepo
from app.schemas import FocusStepCreate


class FocusStepService:
    def __init__(self, focus_step_repo: FocusStepRepo, day_repo: DayRepo) -> None:
        self.focus_step_repo = focus_step_repo
        self.day_repo = day_repo
    
    def _get_day_or_404(self, day_id):
        day = self.day_repo.get_day(day_id)
        if not day:
            raise DayNotFoundError()
        return day

    def _ensure_day_ownership(self, day: Day, user_id: int) -> None:
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def _ensure_step_ownership(self, user_id:int, step: BaseStep):
        if not step.day:
            day = self._get_day_or_404(step.day_id)
        else:
            day = step.day
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def create_focus_step(
        self, focus_step: FocusStepCreate, user_id: int, day_id
    ):
        day = self._get_day_or_404(day_id)
        self._ensure_day_ownership(day, user_id)

        new_focus_step = FocusStep(day_id=day_id, **focus_step.model_dump())
        try: 
            return self.focus_step_repo.create_focus_step(new_focus_step)
        except IntegrityError as exc:
            raise DayNotFoundError() from exc