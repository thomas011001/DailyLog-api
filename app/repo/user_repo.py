from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.models import Day, User


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user):
        new_user = user
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def username_exists(self, username):
        stmt = select(exists().where(User.username == username))
        return self.db.scalar(stmt)

    def get_user_by_username(self, username):
        stmt = select(User).where(User.username == username)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_user_days(self, user_id):
        stmt = select(Day).where(Day.user_id == user_id)
        return self.db.execute(stmt).scalars().all()
