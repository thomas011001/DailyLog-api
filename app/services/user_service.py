from app.repo.user_repo import UserRepo
from app.models import Day


class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def get_user_days(self, user_id: int) -> list[Day]:
        return self.user_repo.get_user_days(user_id)
