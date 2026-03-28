import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import BreakStep, Day, User


@pytest.fixture
def test_user(db_session: Session):
    user = User(username="break_user", password_hash="hashed_pw")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User):
    return {"Authorization": f"Bearer {test_user.token}"}


@pytest.fixture
def test_day(db_session: Session, test_user: User):
    day = Day(owner=test_user, date=datetime.date(2025, 6, 1))
    db_session.add(day)
    db_session.commit()
    db_session.refresh(day)
    return day


@pytest.fixture
def other_user(db_session: Session):
    user = User(username="break_other_user", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def existing_break_step(db_session: Session, test_day: Day):
    step = BreakStep(day=test_day, order=1, description="Coffee break")
    db_session.add(step)
    db_session.commit()
    db_session.refresh(step)
    return step


class TestCreateBreakStep:
    def test_create_break_step_success(self, client: TestClient, auth_headers, test_day):
        res = client.post(
            f"/days/{test_day.id}/break-steps",
            json={"description": "Coffee break"},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_201_CREATED
        body = res.json()
        assert body["description"] == "Coffee break"
        assert body["is_completed"] is False
        assert body["type_identity"] == "break"

    def test_create_break_step_no_description(
        self, client: TestClient, auth_headers, test_day
    ):
        res = client.post(
            f"/days/{test_day.id}/break-steps",
            json={},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_201_CREATED
        assert res.json()["description"] is None

    def test_create_break_step_order_increments(
        self, client: TestClient, auth_headers, test_day
    ):
        res1 = client.post(
            f"/days/{test_day.id}/break-steps",
            json={"description": "First break"},
            headers=auth_headers,
        )
        res2 = client.post(
            f"/days/{test_day.id}/break-steps",
            json={"description": "Second break"},
            headers=auth_headers,
        )
        assert res1.json()["order"] == 1
        assert res2.json()["order"] == 2

    def test_create_break_step_invalid_day(self, client: TestClient, auth_headers):
        res = client.post(
            "/days/9999/break-steps",
            json={"description": "Coffee"},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_create_break_step_without_auth(self, client: TestClient, test_day):
        res = client.post(
            f"/days/{test_day.id}/break-steps",
            json={"description": "Coffee"},
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_break_step_other_user_day(
        self, client: TestClient, test_day, other_user: User
    ):
        res = client.post(
            f"/days/{test_day.id}/break-steps",
            json={"description": "Coffee"},
            headers=other_user.auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN


class TestEditBreakStep:
    def test_edit_break_step_success(
        self, client: TestClient, auth_headers, existing_break_step: BreakStep
    ):
        res = client.put(
            f"/break-steps/{existing_break_step.id}",
            json={"description": "Updated break"},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["description"] == "Updated break"

    def test_edit_break_step_clear_description(
        self, client: TestClient, auth_headers, existing_break_step: BreakStep
    ):
        res = client.put(
            f"/break-steps/{existing_break_step.id}",
            json={"description": None},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["description"] is None

    def test_edit_nonexistent_break_step(self, client: TestClient, auth_headers):
        res = client.put(
            "/break-steps/9999",
            json={"description": "Updated"},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_edit_break_step_without_auth(
        self, client: TestClient, existing_break_step: BreakStep
    ):
        res = client.put(
            f"/break-steps/{existing_break_step.id}",
            json={"description": "Updated"},
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_edit_break_step_other_user(
        self, client: TestClient, existing_break_step: BreakStep, other_user: User
    ):
        res = client.put(
            f"/break-steps/{existing_break_step.id}",
            json={"description": "Hacked"},
            headers=other_user.auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN