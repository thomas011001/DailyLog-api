import os

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
import jwt
import pytest
from app.models import User
from app.utiles import hash_password

load_dotenv()


class TestSignUp:
    # signup success case
    def test_signup_success(self, client):
        response = client.post(
            "/signup",
            json={
                "first_name": "Thomas",
                "last_name": "Doe",
                "username": "thomas",
                "password": "Foo123456",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    # signup fail case
    def test_signup_fail(self, client, db_session):
        db_session.add(User(username="thomas", password_hash="123"))
        db_session.commit()
        response = client.post(
            "/signup",
            json={
                "first_name": "Thomas",
                "last_name": "Doe",
                "username": "thomas",
                "password": "Foo123456",
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "first_name": "",
                "last_name": "Doe",
                "username": "thomas",
                "password": "Foo123456",
            },
            {
                "first_name": "Thomas",
                "last_name": "",
                "username": "thomas",
                "password": "Foo123456",
            },
            {
                "first_name": "Thomas",
                "last_name": "Doe",
                "username": "",
                "password": "Foo123456",
            },
            {
                "first_name": "Thomas",
                "last_name": "Doe",
                "username": "thomas",
                "password": "",
            },
            {"first_name": "", "last_name": "", "username": "", "password": ""},
        ],
    )
    def test_signup_empty_fields(self, client, payload):
        response = client.post("/signup", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize(
        "payload",
        [
            {
                "first_name": "T",
                "last_name": "Doe",
                "username": "thomas",
                "password": "Foo123456",
            },
            {
                "first_name": "Thomas",
                "last_name": "D",
                "username": "thomas",
                "password": "Foo123456",
            },
            {
                "first_name": "Thomas",
                "last_name": "Doe",
                "username": "t",
                "password": "Foo123456",
            },
            {
                "first_name": "Thomas",
                "last_name": "Doe",
                "username": "thomas",
                "password": "F",
            },
        ],
    )
    def test_signup_short_fields(self, client, payload):
        response = client.post("/signup", json=payload)
        print(response.json())
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLogin:
    @pytest.fixture
    def registered_user(self, db_session):
        user = User(username="thomas", password_hash=hash_password("Foo1234"))
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    # --- Success case ---
    def test_login_success(self, client, registered_user):
        response = client.post(
            "/login", json={"username": "thomas", "password": "Foo1234"}
        )
        token = jwt.decode(
            response.json()["token"],
            key=os.getenv("ACCESS_TOKEN_KEY", "very secret key"),
            algorithms=["HS256"],
        )

        assert response.status_code == status.HTTP_200_OK
        assert token["username"] == registered_user.username
        assert token["id"] == registered_user.id
        assert "exp" in token

    # --- Fail case 1: wrong password ---

    def test_login_wrong_password(self, client, registered_user):
        response = client.post(
            "/login", json={"username": "thomas", "password": "Foo123"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Invalid username or password"

    # --- Fail case 2: wrong username ---

    def test_login_wrong_username(self, client, registered_user):
        response = client.post(
            "/login", json={"username": "thomass", "password": "Foo1234"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Invalid username or password"

    # --- Fail case 3: user does not exist ---

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/login", json={"username": "ghost", "password": "Foo1234"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Invalid username or password"

    # --- Fail case 4: empty fields ---

    @pytest.mark.parametrize(
        "payload",
        [
            {"username": "", "password": "Foo1234"},
            {"username": "thomas", "password": ""},
            {"username": "", "password": ""},
        ],
    )
    def test_login_empty_fields(self, client, payload):
        response = client.post("/login", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # --- Fail case 5: username case sensitivity ---

    def test_login_username_case_sensitive(self, client, registered_user):
        response = client.post(
            "/login", json={"username": "Thomas", "password": "Foo1234"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
