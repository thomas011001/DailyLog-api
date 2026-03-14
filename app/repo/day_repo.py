from datetime import date

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from app.models import Day, User


class DayRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_day(self, id: int):
        day = self.db.query(Day).filter(Day.id == id).one()
        return day

    def create_day(self, day):
        new_day = day
        self.db.add(new_day)
        self.db.commit()
        self.db.refresh(new_day)
        return new_day

    def delete_day(self, day: Day):
        self.db.delete(day)
        self.db.commit()
        return day

    def get_day_content(self, id):
        day = (
            self.db.query(Day)
            .options(joinedload(Day.tasks), joinedload(Day.notes))
            .filter(Day.id == id)
            .one()
        )
        return day

    def update_day(self, day: Day, title: str | None = None, date: date | None = None):
        if title is not None:
            day.title = title  # type: ignore
        if date is not None:
            day.date = date  # type: ignore
        self.db.commit()
        self.db.refresh(day)
        return day
