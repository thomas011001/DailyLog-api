from datetime import date as date_type

from sqlalchemy.exc import IntegrityError, NoResultFound

from app.exception import DayNotFoundError, DayConflictError, ForbiddenDayAccessError
from app.models import Day
from app.repo.day_repo import DayRepo
from app.schemas import CreateDay, UpdateDay


class DayService:
    def __init__(self, day_repo: DayRepo):
        self.day_repo = day_repo

    def is_day_exists(self, user_id, date):
        return self.day_repo.is_day_exists(date, user_id)

    def _ensure_ownership(self, day: Day, user_id: int) -> None:
        if day.user_id != user_id:
            raise ForbiddenDayAccessError()

    def create_day(self, user_id: int, payload: CreateDay) -> Day:
        is_day_exists = self.is_day_exists(user_id, payload.date)
        if is_day_exists:
            raise DayConflictError()

        day = Day(user_id=user_id, **payload.model_dump())
        try:
            return self.day_repo.create_day(day)
        except IntegrityError as exc:
            raise DayConflictError() from exc

    def get_day_or_404(self, day_id: int) -> Day:
        day = self.day_repo.get_day(day_id)
        if not day:
            raise DayNotFoundError()
        return day

    def delete_day(self, day_id: int, user_id: int) -> Day:
        day = self.get_day_or_404(day_id)
        self._ensure_ownership(day, user_id)
        self.day_repo.delete_day(day)
        return day

    def get_day_content(self, day_id: int, user_id: int) -> Day:
        day = self.get_day_or_404(day_id)
        self._ensure_ownership(day, user_id)
        return self.day_repo.get_day_content(day)

    def edit_day(self, day_id: int, user_id: int, payload: UpdateDay) -> Day:
        day = self.get_day_or_404(day_id)
        self._ensure_ownership(day, user_id)

        try:
            return self.day_repo.update_day(
                day, title=payload.title, date=payload.new_date
            )
        except IntegrityError as exc:
            raise DayConflictError() from exc
