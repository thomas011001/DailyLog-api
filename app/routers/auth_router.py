from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_user_repo
from app.repo.user_repo import UserRepo
from app.schemas import CreateUser, UserOut, Credentials
from app.services.auth_service import (
    AuthService,
    InvalidCredentialsError,
    UsernameTakenError,
)

auth_router = APIRouter()


@auth_router.post(
    "/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
def create_user(user: CreateUser, repo: UserRepo = Depends(get_user_repo)):
    service = AuthService(repo)
    try:
        new_user = service.register_user(user)
    except UsernameTakenError:
        raise HTTPException(status.HTTP_409_CONFLICT, "This username is taken.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Could not create the user."
        )

    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: Credentials, repo: UserRepo = Depends(get_user_repo)):
    service = AuthService(repo)
    try:
        token = service.authenticate(credentials)
    except InvalidCredentialsError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid username or password")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error."
        )

    return {"token": token}
