import datetime

import pytest
from sqlalchemy.orm import Session
from fastapi import status

from app.models import Day, Day, User


@pytest.fixture
def test_user(db_session: Session):
    user = User(username="test_user", password_hash="hashed_pw")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User):
    return {"Authorization": f"Bearer {test_user.token}"}


@pytest.fixture
def test_day(db_session: Session, test_user):
    day = Day(owner=test_user, date=datetime.datetime(2025, 5, 5))
    db_session.add(day)
    db_session.commit()
    db_session.refresh(day)
    return day


@pytest.fixture
def other_user(db_session: Session):
    user = User(username="Moo", password_hash="Moooooooooo")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestCreateFocusSteps:
    def test_create_focus_steps_success(self, client, test_day, auth_headers):
        response = client.post(
            f"/days/{test_day.id}/focus-steps",
            json={"sessions_count": 3},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        order1 = response.json()["order"]
        assert order1 == 1
        response = client.post(
            f"/days/{test_day.id}/focus-steps",
            json={"sessions_count": 3},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        order2 = response.json()["order"]
        assert order2 == 2

    def test_create_focus_steps_invalid_day(self, client, test_day, auth_headers):
        response = client.post(
            f"/days/{test_day.id + 1}/focus-steps",
            json={"sessions_count": 3},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_focus_steps_without_auth_user(self, client, test_day):
        res = client.post(f"/days/{test_day.id}/focus-steps", json={"session_count": 1})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_focus_steps_no_ownership_day(
        self, client, test_day, other_user: User
    ):
        res = client.post(
            f"/days/{test_day.id}/focus-steps",
            json={"session_count": 1},
            headers=other_user.auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_create_focus_steps_response_shape(self, client, test_day, auth_headers):
        response = client.post(
            f"/days/{test_day.id}/focus-steps",
            json={"sessions_count": 3},
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["sessions_count"] == 3
        assert len(data["sessions"]) == 3
        assert all(s["is_completed"] is False for s in data["sessions"])

    def test_create_focus_steps_invalid_payload(self, client, test_day, auth_headers):
        response = client.post(
            f"/days/{test_day.id}/focus-steps",
            json={"sessions_count": -1},  # or omit the field entirely
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY