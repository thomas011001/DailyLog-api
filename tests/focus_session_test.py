import datetime

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.models import Day, FocusSession, FocusStep, User


@pytest.fixture
def focus_session(db_session: Session, test_focus_step: FocusStep):
    session = FocusSession(focus_step_id=test_focus_step.id)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session


@pytest.fixture
def other_user(db_session: Session):
    user = User(username="other_session_user", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestCreateFocusSession:
    def test_create_session_success(
        self, client: TestClient, auth_headers, test_focus_step: FocusStep
    ):
        res = client.post(
            f"/focus_steps/{test_focus_step.id}/sessions", headers=auth_headers
        )
        assert res.status_code == status.HTTP_201_CREATED
        body = res.json()
        assert "id" in body
        assert body["is_completed"] is False

    def test_create_session_invalid_step(self, client: TestClient, auth_headers):
        res = client.post("/focus_steps/9999/sessions", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_create_session_without_auth(
        self, client: TestClient, test_focus_step: FocusStep
    ):
        res = client.post(f"/focus_steps/{test_focus_step.id}/sessions")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_session_other_user_step(
        self, client: TestClient, test_focus_step: FocusStep, other_user: User
    ):
        res = client.post(
            f"/focus_steps/{test_focus_step.id}/sessions",
            headers=other_user.auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN


class TestDeleteFocusSession:
    def test_delete_session_success(
        self, client: TestClient, auth_headers, focus_session: FocusSession
    ):
        res = client.delete(f"/sessions/{focus_session.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["detail"] == "Session deleted."

    def test_delete_nonexistent_session(self, client: TestClient, auth_headers):
        res = client.delete("/sessions/9999", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_session_without_auth(
        self, client: TestClient, focus_session: FocusSession
    ):
        res = client.delete(f"/sessions/{focus_session.id}")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_session_other_user(
        self,
        client: TestClient,
        focus_session: FocusSession,
        other_user: User,
    ):
        res = client.delete(
            f"/sessions/{focus_session.id}", headers=other_user.auth_headers
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_already_deleted_session(
        self, client: TestClient, auth_headers, focus_session: FocusSession
    ):
        client.delete(f"/sessions/{focus_session.id}", headers=auth_headers)
        res = client.delete(f"/sessions/{focus_session.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND


class TestToggleFocusSession:
    def test_toggle_session_success(
        self, client: TestClient, auth_headers, focus_session: FocusSession
    ):
        res = client.patch(
            f"/sessions/{focus_session.id}/toggle", headers=auth_headers
        )
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["is_completed"] is True

    def test_toggle_session_twice(
        self, client: TestClient, auth_headers, focus_session: FocusSession
    ):
        client.patch(f"/sessions/{focus_session.id}/toggle", headers=auth_headers)
        res = client.patch(
            f"/sessions/{focus_session.id}/toggle", headers=auth_headers
        )
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["is_completed"] is False

    def test_toggle_nonexistent_session(self, client: TestClient, auth_headers):
        res = client.patch("/sessions/9999/toggle", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_toggle_session_without_auth(
        self, client: TestClient, focus_session: FocusSession
    ):
        res = client.patch(f"/sessions/{focus_session.id}/toggle")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_toggle_session_other_user(
        self,
        client: TestClient,
        focus_session: FocusSession,
        other_user: User,
    ):
        res = client.patch(
            f"/sessions/{focus_session.id}/toggle", headers=other_user.auth_headers
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN