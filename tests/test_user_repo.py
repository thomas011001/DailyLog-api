from app.models import User
from app.repo.user import UserRepo

def test_create_user(db_session):
  repo = UserRepo(db_session)
  user = repo.create_user({"username": "thomas", "password_hash": "thomas"})
  assert user.id is not None
  assert user.username == "thomas" # type: ignore
  assert db_session.query(User).filter(User.username == "thomas").first() == user

def test_username_exists(db_session, ):
  repo = UserRepo(db_session)
  db_session.add(User(username="thomas", password_hash="123"))
  assert repo.username_exists("thomas") == True
  assert repo.username_exists("yacoub") == False
