from datetime import date, datetime

from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.models import User, Day, Task


class TestCreateTask:
    def test_create_task_success(self, client: TestClient, task_auth_headers, task_day):
        res = client.post(
            f"/days/{task_day.id}/tasks",
            json={
                "title": "New Task",
            },
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_201_CREATED
        body = res.json()
        assert body["title"] == "New Task"

    def test_create_task_invalid_day(self, client: TestClient, task_auth_headers):
        res = client.post(
            "/days/9999/tasks",
            json={"title": "New Task"},
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_create_task_day_of_other_user(
        self, client: TestClient, db_session, task_auth_headers
    ):
        other_user = User(username="other", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        other_day = Day(owner=other_user, date=date(2025, 6, 1))
        db_session.add(other_day)
        db_session.commit()

        res = client.post(
            f"days/{other_day.id}/tasks",
            json={"title": "Hack"},
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_create_task_unauthenticated(self, client: TestClient, task_day: Day):
        res = client.post(
            f"days/{task_day.id}/tasks",
            json={"title": "New Task"},
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestEditTask:
    def test_edit_task_success(
        self,
        client: TestClient,
        task_auth_headers,
        existing_task: Task,
    ):
        res = client.put(
            f"/tasks/{existing_task.id}",
            json={
                "title": "Updated",
            },
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_200_OK
        body = res.json()
        assert body["id"] == existing_task.id
        assert body["title"] == "Updated"

    def test_edit_nonexistent_task(self, client: TestClient, task_auth_headers):
        res = client.put(
            "/tasks/9999",
            json={"title": "Updated"},
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_edit_task_of_other_user(
        self,
        client: TestClient,
        db_session: Session,
        task_auth_headers,
        task_day: Day,
    ):
        other_user = User(username="other_user", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        other_day = Day(owner=other_user, date=date(2025, 7, 1))
        db_session.add(other_day)
        db_session.commit()
        other_task = Task(day=other_day, title="Other's task")
        db_session.add(other_task)
        db_session.commit()
        db_session.refresh(other_task)

        res = client.put(
            f"/tasks/{other_task.id}",
            json={"title": "Hacked"},
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_edit_task_without_auth(self, client: TestClient, existing_task: Task):
        res = client.put(
            f"/tasks/{existing_task.id}",
            json={"title": "Updated"},
        )
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeleteTask:
    def test_delete_task_success(
        self,
        client: TestClient,
        task_auth_headers,
        existing_task: Task,
    ):
        res = client.delete(f"/tasks/{existing_task.id}", headers=task_auth_headers)
        assert res.status_code == status.HTTP_200_OK

    def test_delete_nonexistent_task(self, client: TestClient, task_auth_headers):
        res = client.delete("/tasks/9999", headers=task_auth_headers)
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_task_of_other_user(
        self,
        client: TestClient,
        db_session: Session,
        task_auth_headers,
        task_day: Day,
    ):
        other_user = User(username="other_user2", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        other_day = Day(owner=other_user, date=date(2025, 8, 1))
        db_session.add(other_day)
        db_session.commit()
        other_task = Task(day=other_day, title="Other's task")
        db_session.add(other_task)
        db_session.commit()
        db_session.refresh(other_task)

        res = client.delete(
            f"/tasks/{other_task.id}",
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_task_without_auth(self, client: TestClient, existing_task: Task):
        res = client.delete(f"/tasks/{existing_task.id}")
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
