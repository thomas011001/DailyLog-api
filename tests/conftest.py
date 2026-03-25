import datetime

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient

from app.core.db import Base, get_db
from app.main import app
from app.models import Day, FocusSession, Task, User

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

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
def test_focus_step(db_session: Session, test_day: Day):
    session = FocusSession(day=test_day)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session


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
    day = Day(owner=task_user, date=datetime.date(2025, 5, 5))
    db_session.add(day)
    db_session.commit()
    db_session.refresh(day)
    return day


@pytest.fixture
def existing_task(db_session: Session, task_day: Day):
    task = Task(day=task_day, title="Initial")
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task