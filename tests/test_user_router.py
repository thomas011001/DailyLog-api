import datetime
import os

from dotenv import load_dotenv
import jwt
import pytest
from unittest.mock import MagicMock
from fastapi import status
from app.models import User, Day
from app.utiles import hash_password
from app.dependancies import get_current_user, get_user_repo

# --- Fixtures ---
load_dotenv()


@pytest.fixture
def registered_user(db_session):
    user = User(username="thomas", password_hash=hash_password("Foo1234"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(registered_user):
    """Generate a valid JWT token for the registered user."""
    token = registered_user.token
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_days(registered_user, db_session):
    """Create some days belonging to the registered user."""
    days = [
        Day(date=datetime.date(2024, 1, 1), user_id=registered_user.id),
        Day(date=datetime.date(2024, 1, 2), user_id=registered_user.id),
    ]
    db_session.add_all(days)
    db_session.commit()
    return days


# --- Test class ---


class TestGetCurrentUserDays:

    # success: returns the user's days
    def test_returns_user_days(self, client, auth_headers, registered_user, user_days):
        response = client.get("/me/days", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == len(user_days)

    # success: returns empty list when user has no days
    def test_returns_empty_list_when_no_days(self, client, auth_headers):
        response = client.get("/me/days", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    # fail: no token provided
    def test_unauthenticated_request_fails(self, client):
        response = client.get("/me/days")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # fail: invalid/malformed token
    def test_invalid_token_fails(self, client):
        response = client.get(
            "/me/days", headers={"Authorization": "Bearer not.a.real.token"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # fail: expired token
    def test_expired_token_fails(self, client, registered_user):
        expired_token = jwt.encode(
            {
                "id": registered_user.id,
                "username": registered_user.username,
                "exp": datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(hours=1),
            },
            os.getenv("ACCESS_TOKEN_KEY", "very secret key"),
        )
        response = client.get(
            "/me/days", headers={"Authorization": f"Bearer {expired_token}"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # fail: days only belong to the requesting user, not other users
    def test_does_not_return_other_users_days(self, client, auth_headers, db_session):
        other_user = User(username="other", password_hash=hash_password("Bar5678"))
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)

        other_day = Day(date=datetime.date(2024, 5, 6), user_id=other_user.id)
        db_session.add(other_day)
        db_session.commit()

        response = client.get("/me/days", headers=auth_headers)

        returned_user_ids = {day["user_id"] for day in response.json()}
        assert other_user.id not in returned_user_ids
