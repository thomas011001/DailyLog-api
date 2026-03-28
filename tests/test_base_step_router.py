import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import BreakStep, Day, FocusStep, User


@pytest.fixture
def test_user(db_session: Session):
    user = User(username="base_step_user", password_hash="hashed_pw")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User):
    return {"Authorization": f"Bearer {test_user.token}"}


@pytest.fixture
def test_day(db_session: Session, test_user: User):
    day = Day(owner=test_user, date=datetime.date(2025, 7, 1))
    db_session.add(day)
    db_session.commit()
    db_session.refresh(day)
    return day


@pytest.fixture
def other_user(db_session: Session):
    user = User(username="base_step_other", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def focus_step(db_session: Session, test_day: Day):
    step = FocusStep(day=test_day, order=1)
    db_session.add(step)
    db_session.commit()
    db_session.refresh(step)
    return step


@pytest.fixture
def break_step(db_session: Session, test_day: Day):
    step = BreakStep(day=test_day, order=2, description="Coffee")
    db_session.add(step)
    db_session.commit()
    db_session.refresh(step)
    return step


class TestDeleteStep:
    def test_delete_focus_step_success(
        self, client: TestClient, auth_headers, focus_step: FocusStep
    ):
        res = client.delete(f"/steps/{focus_step.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["detail"] == "Step deleted."

    def test_delete_break_step_success(
        self, client: TestClient, auth_headers, break_step: BreakStep
    ):
        res = client.delete(f"/steps/{break_step.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["detail"] == "Step deleted."

    def test_delete_nonexistent_step(self, client: TestClient, auth_headers):
        res = client.delete("/steps/9999", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_step_without_auth(self, client: TestClient, focus_step: FocusStep):
        res = client.delete(f"/steps/{focus_step.id}")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_step_other_user(
        self, client: TestClient, focus_step: FocusStep, other_user: User
    ):
        res = client.delete(
            f"/steps/{focus_step.id}", headers=other_user.auth_headers
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_already_deleted_step(
        self, client: TestClient, auth_headers, focus_step: FocusStep
    ):
        client.delete(f"/steps/{focus_step.id}", headers=auth_headers)
        res = client.delete(f"/steps/{focus_step.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND


class TestToggleStep:
    def test_toggle_focus_step_success(
        self, client: TestClient, auth_headers, focus_step: FocusStep
    ):
        res = client.patch(f"/steps/{focus_step.id}/toggle", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["is_completed"] is True

    def test_toggle_break_step_success(
        self, client: TestClient, auth_headers, break_step: BreakStep
    ):
        res = client.patch(f"/steps/{break_step.id}/toggle", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["is_completed"] is True

    def test_toggle_step_twice(
        self, client: TestClient, auth_headers, focus_step: FocusStep
    ):
        client.patch(f"/steps/{focus_step.id}/toggle", headers=auth_headers)
        res = client.patch(f"/steps/{focus_step.id}/toggle", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["is_completed"] is False

    def test_toggle_nonexistent_step(self, client: TestClient, auth_headers):
        res = client.patch("/steps/9999/toggle", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_toggle_step_without_auth(self, client: TestClient, focus_step: FocusStep):
        res = client.patch(f"/steps/{focus_step.id}/toggle")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_toggle_step_other_user(
        self, client: TestClient, focus_step: FocusStep, other_user: User
    ):
        res = client.patch(
            f"/steps/{focus_step.id}/toggle", headers=other_user.auth_headers
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN