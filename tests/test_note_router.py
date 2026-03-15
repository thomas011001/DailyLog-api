from datetime import date

from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.models import User, Day, Note


@pytest.fixture
def note_user(db_session: Session):
    user = User(username="note_user", password_hash="hashed_pw")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def note_auth_headers(note_user: User):
    return {"Authorization": f"Bearer {note_user.token}"}


@pytest.fixture
def note_day(db_session: Session, note_user: User):
    day = Day(owner=note_user, date=date(2025, 5, 6))
    db_session.add(day)
    db_session.commit()
    db_session.refresh(day)
    return day


@pytest.fixture
def existing_note(db_session: Session, note_day: Day):
    note = Note(day=note_day, content="initial")
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)
    return note


class TestCreateNote:
    def test_create_note_success(
        self, client: TestClient, note_auth_headers, note_day: Day
    ):
        res = client.post(
            "/notes",
            json={"day_id": note_day.id, "content": "hello"},
            headers=note_auth_headers,
        )
        assert res.status_code == status.HTTP_201_CREATED
        body = res.json()
        assert body["content"] == "hello"

    def test_create_note_invalid_day(self, client: TestClient, note_auth_headers):
        res = client.post(
            "/notes",
            json={"day_id": 9999, "content": "hello"},
            headers=note_auth_headers,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_create_note_day_of_other_user(
        self, client: TestClient, db_session: Session, note_auth_headers
    ):
        other_user = User(username="other_note_user", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        other_day = Day(owner=other_user, date=date(2025, 6, 2))
        db_session.add(other_day)
        db_session.commit()

        res = client.post(
            "/notes",
            json={"day_id": other_day.id, "content": "hack"},
            headers=note_auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_create_note_unauthenticated(self, client: TestClient, note_day: Day):
        res = client.post(
            "/notes",
            json={"day_id": note_day.id, "content": "hello"},
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestEditNote:
    def test_edit_note_success(
        self,
        client: TestClient,
        note_auth_headers,
        existing_note: Note,
    ):
        res = client.put(
            f"/notes/{existing_note.id}",
            json={"content": "updated"},
            headers=note_auth_headers,
        )
        assert res.status_code == status.HTTP_200_OK
        body = res.json()
        assert body["id"] == existing_note.id
        assert body["content"] == "updated"

    def test_edit_nonexistent_note(self, client: TestClient, note_auth_headers):
        res = client.put(
            "/notes/9999",
            json={"content": "updated"},
            headers=note_auth_headers,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_edit_note_of_other_user(
        self,
        client: TestClient,
        db_session: Session,
        note_auth_headers,
        note_day: Day,
    ):
        other_user = User(username="other_note_user2", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        other_day = Day(owner=other_user, date=date(2025, 7, 2))
        db_session.add(other_day)
        db_session.commit()
        other_note = Note(day=other_day, content="other's")
        db_session.add(other_note)
        db_session.commit()
        db_session.refresh(other_note)

        res = client.put(
            f"/notes/{other_note.id}",
            json={"content": "hacked"},
            headers=note_auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_edit_note_without_auth(self, client: TestClient, existing_note: Note):
        res = client.put(
            f"/notes/{existing_note.id}",
            json={"content": "updated"},
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeleteNote:
    def test_delete_note_success(
        self,
        client: TestClient,
        note_auth_headers,
        existing_note: Note,
    ):
        res = client.delete(f"/notes/{existing_note.id}", headers=note_auth_headers)
        assert res.status_code == status.HTTP_200_OK

    def test_delete_nonexistent_note(self, client: TestClient, note_auth_headers):
        res = client.delete("/notes/9999", headers=note_auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_note_of_other_user(
        self,
        client: TestClient,
        db_session: Session,
        note_auth_headers,
        note_day: Day,
    ):
        other_user = User(username="other_note_user3", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        other_day = Day(owner=other_user, date=date(2025, 8, 2))
        db_session.add(other_day)
        db_session.commit()
        other_note = Note(day=other_day, content="other's")
        db_session.add(other_note)
        db_session.commit()
        db_session.refresh(other_note)

        res = client.delete(
            f"/notes/{other_note.id}",
            headers=note_auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_note_without_auth(self, client: TestClient, existing_note: Note):
        res = client.delete(f"/notes/{existing_note.id}")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

