from sqlalchemy.exc import IntegrityError

from app.exception import (
    DayNotFoundError,
    ForbiddenDayAccessError,
    SessionNotFoundError,
    StepNotFoundError,
)
from app.models import BaseStep, FocusSession
from app.repo.day_repo import DayRepo
from app.repo.focus_session_repo import FocusSessionRepo
from app.repo.step_repo import BaseStepRepo


class FocusSessionService:
    def __init__(
        self,
        session_repo: FocusSessionRepo,
        base_step_repo: BaseStepRepo,
        day_repo: DayRepo,
    ):
        self.session_repo = session_repo
        self.base_step_repo = base_step_repo
        self.day_repo = day_repo

    def _get_day_or_404(self, day_id):
        day = self.day_repo.get_day(day_id)
        if not day:
            raise DayNotFoundError()
        return day

    def _get_step_or_404(self, step_id: int):
        step = self.base_step_repo.get_step(step_id)
        if not step:
            raise StepNotFoundError()
        return step

    def _get_session_or_404(self, session_id: int):
        session = self.session_repo.get_focus_session(session_id)
        if not session:
            raise SessionNotFoundError()
        return session

    def _ensure_step_ownership(self, user_id: int, step: BaseStep):
        day = step.day if step.day else self._get_day_or_404(step.day_id)
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def _ensure_session_ownership(self, user_id: int, session: FocusSession):
        step = self._get_step_or_404(session.focus_step_id)
        self._ensure_step_ownership(user_id, step)

    def create_session(self, step_id: int, user_id: int):
        step = self._get_step_or_404(step_id)
        self._ensure_step_ownership(user_id, step)

        new_session = FocusSession(focus_step_id=step.id)
        try:
            return self.session_repo.create_focus_session(new_session)
        except IntegrityError:
            raise StepNotFoundError()

    def delete_session(self, session_id: int, user_id: int):
        session = self._get_session_or_404(session_id)
        self._ensure_session_ownership(user_id, session)
        return self.session_repo.delete_focus_session(session)

    def toggle_session(self, session_id: int, user_id: int):
        session = self._get_session_or_404(session_id)
        self._ensure_session_ownership(user_id, session)
        return self.session_repo.toggle_focus_session(session)