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
        return (
            True
            if self.db.query(User).filter(User.username == username).first()
            else False
        )

    def get_user_by_username(self, username):
        return self.db.query(User).filter(User.username == username).first()

    def get_user_days(self, id):
        return self.db.query(Day).filter(Day.user_id == id).all()
