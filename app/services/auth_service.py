from sqlalchemy.exc import IntegrityError

from app.exception import UsernameTakenError, InvalidCredentialsError
from app.models import User
from app.repo.user_repo import UserRepo
from app.schemas import CreateUser, Credentials
from app.utiles import hash_password, verify_password


class AuthService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def register_user(self, user_in: CreateUser) -> User:
        is_username_taken = self.user_repo.username_exists(user_in.username)
        if is_username_taken:
            raise UsernameTakenError()

        hashed_password = hash_password(user_in.password)
        user = User(
            **user_in.model_dump(exclude={"password"}),
            password_hash=hashed_password,
        )

        try:
            return self.user_repo.create_user(user)
        except IntegrityError as exc:
            raise UsernameTakenError() from exc

    def authenticate(self, credentials: Credentials) -> str:
        user = self.user_repo.get_user_by_username(credentials.username)
        if not user:
            raise InvalidCredentialsError()

        correct_passwrod = verify_password(credentials.password, user.password_hash)
        if not correct_passwrod:
            raise InvalidCredentialsError()

        return user.token
