import pytest

from app.models import User
from app.repo.user_repo import UserRepo


@pytest.fixture
def repo(db_session):
    return UserRepo(db_session)


def test_create_user(db_session, repo):
    user = repo.create_user(User(username="thomas", password_hash="Foo123"))

    assert user.id is not None
    assert user.username == "thomas"  # type: ignore

    assert db_session.query(User).filter(User.username == "thomas").first() == user


def test_username_exists(db_session, repo):
    db_session.add(User(username="thomas", password_hash="123"))
    db_session.commit()
    assert repo.username_exists("thomas") == True
    assert repo.username_exists("yacoub") == False


def test_get_user_by_username(db_session, repo):
    user = User(username="thomas", password_hash="123")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    assert repo.get_user_by_username("thomas").id == user.id
    assert repo.get_user_by_username("Foo") is None
