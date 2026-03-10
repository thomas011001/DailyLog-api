from sqlalchemy.orm import Session

from app.models import User


class UserRepo:
  def __init__(self, db: Session):
    self.db = db

  def create_user(self, user_data: dict):
    user = User(**user_data)
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)
    return user
  
  def username_exists(self, username):
    return True if self.db.query(User).filter(User.username == username).first() else False
  
  def get_user_by_username(self, username):
    return self.db.query(User).filter(User.username == username).first()
  