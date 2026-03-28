class UsernameTakenError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class DayNotFoundError(Exception):
    pass


class StepNotFoundError(Exception):
    pass


class DayConflictError(Exception):
    pass


class ForbiddenDayAccessError(Exception):
    pass


class TaskNotFoundError(Exception):
    pass


class SessionNotFoundError(Exception):
    pass