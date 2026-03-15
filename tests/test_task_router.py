from datetime import date, datetime

from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from app.models import User, Day, Task


@pytest.fixture
def task_user(db_session: Session):
    user = User(username="task_user", password_hash="hashed_pw")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def task_auth_headers(task_user: User):
    return {"Authorization": f"Bearer {task_user.token}"}


@pytest.fixture
def task_day(db_session: Session, task_user: User):
    day = Day(owner=task_user, date=date(2025, 5, 5))
    db_session.add(day)
    db_session.commit()
    db_session.refresh(day)
    return day


@pytest.fixture
def existing_task(db_session: Session, task_day: Day):
    task = Task(day=task_day, title="Initial", description="desc", priority=1)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


class TestCreateTask:
    def test_create_task_success(self, client: TestClient, task_auth_headers, task_day):
        res = client.post(
            "/tasks",
            json={
                "day_id": task_day.id,
                "title": "New Task",
                "description": "Do something",
                "priority": 2,
                "remind_at": datetime(2025, 5, 5, 12, 0, 0).isoformat(),
            },
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_201_CREATED
        body = res.json()
        assert body["title"] == "New Task"
        assert body["priority"] == 2

    def test_create_task_invalid_day(self, client: TestClient, task_auth_headers):
        res = client.post(
            "/tasks",
            json={"day_id": 9999, "title": "New Task"},
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND

    def test_create_task_day_of_other_user(self, client: TestClient, db_session, task_auth_headers):
        other_user = User(username="other", password_hash="hash")
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        other_day = Day(owner=other_user, date=date(2025, 6, 1))
        db_session.add(other_day)
        db_session.commit()

        res = client.post(
            "/tasks",
            json={"day_id": other_day.id, "title": "Hack"},
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_create_task_unauthenticated(self, client: TestClient, task_day: Day):
        res = client.post(
            "/tasks",
            json={"day_id": task_day.id, "title": "New Task"},
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
            json={"title": "Updated", "priority": 3},
            headers=task_auth_headers,
        )
        assert res.status_code == status.HTTP_200_OK
        body = res.json()
        assert body["id"] == existing_task.id
        assert body["title"] == "Updated"
        assert body["priority"] == 3

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

