from datetime import date
import datetime
import os

from dotenv import load_dotenv
from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.models import User, Day

load_dotenv()


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


class TestCraeteDay:

    def test_create_day_success(self, client, auth_headers):
        res = client.post(
            "/day",
            json={"title": "Foo", "date": date(2024, 5, 30).isoformat()},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_201_CREATED
        res = client.post(
            "/day", json={"date": date(2024, 5, 29).isoformat()}, headers=auth_headers
        )
        assert res.status_code == status.HTTP_201_CREATED

    def test_create_day_repeated_day(self, client, auth_headers, test_day: Day):
        res = client.post(
            "/day",
            json={"title": "Foo", "date": str(test_day.date)},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_409_CONFLICT

    def test_create_day_wrong_date(self, client, auth_headers):
        res = client.post(
            "/day", json={"title": "Foo", "date": "2024"}, headers=auth_headers
        )
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        res2 = client.post(
            "/day", json={"title": "Foo", "date": "hi"}, headers=auth_headers
        )
        assert res2.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        res3 = client.post("/day", json={}, headers=auth_headers)
        assert res3.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_day_without_auth_user(self, client):
        res = client.post(
            "/day",
            json={"title": "Foo", "date": date(2024, 5, 30).isoformat()},
            headers={"Authorization": f"Bearer 123"},
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        res2 = client.post(
            "/day", json={"title": "Foo", "date": date(2024, 5, 30).isoformat()}
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_day_same_date_different_users(
        self, client, db_session, auth_headers
    ):
        other_user = User(username="other", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        day = Day(owner=other_user, date=date(2024, 5, 30))
        db_session.add(day)
        db_session.commit()

        res = client.post("/day", json={"date": "2024-05-30"}, headers=auth_headers)
        assert res.status_code == status.HTTP_201_CREATED

    def test_create_day_response_body(self, client, auth_headers):
        res = client.post(
            "/day",
            json={"title": "Foo", "date": date(2024, 6, 1).isoformat()},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_201_CREATED
        body = res.json()
        assert "id" in body
        assert body["date"] == "2024-06-01"
        assert body["title"] == "Foo"

    def test_create_day_wrong_date_format(self, client, auth_headers):
        res = client.post("/day", json={"date": "2024/05/30"}, headers=auth_headers)
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        res2 = client.post("/day", json={"date": "30-05-2024"}, headers=auth_headers)
        assert res2.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestDeleteDay:
    def test_delete_day_success(
        self, client: TestClient, test_day: Day, db_session: Session, auth_headers
    ):
        res = client.delete(f"/day/{test_day.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK

    def test_delete_nonexist_day(self, client: TestClient, test_day, auth_headers):
        res = client.delete(f"/day/{test_day.id + 5325}", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_day_of_another_user(
        self, client: TestClient, test_day: Day, db_session: Session
    ):
        other_user = User(username="other_user", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)

        other_headers = {"Authorization": f"Bearer {other_user.token}"}
        res = client.delete(f"/day/{test_day.id}", headers=other_headers)
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_day_without_auth(self, client: TestClient, test_day: Day):
        res = client.delete(f"/day/{test_day.id}")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_already_deleted_day(
        self, client: TestClient, test_day: Day, auth_headers
    ):
        client.delete(f"/day/{test_day.id}", headers=auth_headers)
        res = client.delete(f"/day/{test_day.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND


class TestGetDayContent:
    def test_get_day_content_success(
        self, client: TestClient, test_day: Day, auth_headers
    ):
        res = client.get(f"/day/{test_day.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK
        assert res.json()["id"] == test_day.id

    def test_get_nonexist_day_content(self, client: TestClient, test_day, auth_headers):
        res = client.get(f"/day/{test_day.id + 5325}", headers=auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_get_day_content_response_body(
        self, client: TestClient, test_day: Day, auth_headers
    ):
        res = client.get(f"/day/{test_day.id}", headers=auth_headers)
        assert res.status_code == status.HTTP_200_OK
        body = res.json()
        assert body["id"] == test_day.id
        assert "date" in body
        assert "title" in body

    def test_get_day_of_another_user(
        self, client: TestClient, test_day: Day, db_session: Session
    ):
        other_user = User(username="other_user2", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()

        other_headers = {"Authorization": f"Bearer {other_user.token}"}
        res = client.get(f"/day/{test_day.id}", headers=other_headers)
        assert res.status_code == status.HTTP_403_FORBIDDEN


class TestEditDay:
    def test_edit_day_success(
        self, client: TestClient, test_day: Day, db_session: Session, auth_headers
    ):
        new_title = "Updated Title"
        new_date = date(2024, 6, 5).isoformat()
        res = client.put(
            f"/day/{test_day.id}",
            json={"title": new_title, "new_date": new_date},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_200_OK
        body = res.json()
        assert body["id"] == test_day.id
        assert body["title"] == new_title
        assert body["date"] == new_date

    def test_edit_nonexist_day(self, client: TestClient, test_day, auth_headers):
        res = client.put(
            f"/day/{test_day.id + 5325}",
            json={"title": "New Title"},
            headers=auth_headers,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_edit_day_of_another_user(
        self, client: TestClient, test_day: Day, db_session: Session
    ):
        other_user = User(username="other_user3", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()

        other_headers = {"Authorization": f"Bearer {other_user.token}"}
        res = client.put(
            f"/day/{test_day.id}",
            json={"title": "New Title"},
            headers=other_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_edit_day_without_auth(self, client: TestClient, test_day: Day):
        res = client.put(f"/day/{test_day.id}", json={"title": "New Title"})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
