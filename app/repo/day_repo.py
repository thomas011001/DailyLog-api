from datetime import date
import datetime

from sqlalchemy import exists, select
from sqlalchemy.orm import Session, joinedload

from app.models import Day


class DayRepo:
    def __init__(self, db: Session):
        self.db = db

    def is_day_exists(self, date: datetime.date, user_id: int):
        stmt = select(Day.id).where(Day.date == date, Day.user_id == user_id).limit(1)
        return self.db.scalar(stmt) is not None

    def get_day(self, id: int):
        stmt = select(Day).where(Day.id == id)
        return self.db.scalar(stmt)

    def create_day(self, day):
        self.db.add(day)
        self.db.commit()
        self.db.refresh(day)
        return day

    def delete_day(self, day: Day):
        self.db.delete(day)
        self.db.commit()
        return day

    def get_day_content(self, day: Day):
        stmt = select(Day).options(joinedload(Day.tasks)).where(Day.id == day.id)
        return self.db.execute(stmt).unique().scalar_one_or_none()

    def update_day(self, day: Day, title: str | None = None, date: date | None = None):
        if title is not None:
            day.title = title
        if date is not None:
            day.date = date
        self.db.commit()
        self.db.refresh(day)
        return day


# user enter -
# start new day -
# creates a tasks for the day -
# start adding steps to the timeblock
#   - foucs
#   - break
#  finish the foucse sessions
#  finish the foucse and breack steps
#  end the day
