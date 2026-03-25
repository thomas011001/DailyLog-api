class UsernameTakenError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class DayNotFoundError(Exception):
    pass


class DayConflictError(Exception):
    pass


class ForbiddenDayAccessError(Exception):
    pass


class TaskNotFoundError(Exception):
    pass


