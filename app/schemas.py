from datetime import date, datetime
import enum

from pydantic import BaseModel, Field, ConfigDict


class StepType(enum.Enum):
    FOCUS = "focus"
    BREAK = "break"


class CreateUser(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    username: str = Field(min_length=3, max_length=20, pattern=r"^\S+$")
    password: str = Field(min_length=8, max_length=128)

    model_config = ConfigDict(str_strip_whitespace=True)


class UserOut(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class Credentials(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class CreateDay(BaseModel):
    title: str | None = None
    date: date


class TaskOut(BaseModel):
    id: int
    title: str
<<<<<<< HEAD
    description: str | None = None
    priority: int = 1
    remind_at: datetime | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class NoteOut(BaseModel):
    id: int
    content: str

    model_config = ConfigDict(from_attributes=True)


class DayOut(BaseModel):
    id: int
    title: str | None = None
    date: date
    tasks: list[TaskOut]
    notes: list[NoteOut]
=======
    is_complete: bool
>>>>>>> dev

    model_config = ConfigDict(from_attributes=True)


class UpdateDay(BaseModel):
    title: str | None = None
    new_date: date | None = None


class UserTokenData(BaseModel):
    id: int
    username: str


class CreateTask(BaseModel):
    title: str
<<<<<<< HEAD
    description: str | None = None
    priority: int = 1
    remind_at: datetime | None = None
    status: str | None = None
=======
>>>>>>> dev


class UpdateTask(BaseModel):
    title: str | None = None
<<<<<<< HEAD
    description: str | None = None
    priority: int | None = None
    remind_at: datetime | None = None
    status: str | None = None
=======
    is_complete: bool | None = None
>>>>>>> dev


class StepOut(BaseModel):
    id: int
    order: int
    is_completed: bool
    type_identity: str

    model_config = ConfigDict(from_attributes=True)


class FocusSessionOut(BaseModel):
    id: int
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)


class FocusStepOut(StepOut):
    sessions_count: int
    sessions: list[FocusSessionOut]

    model_config = ConfigDict(from_attributes=True)


class BreakStepOut(StepOut):
    description: str

    model_config = ConfigDict(from_attributes=True)


class DayOut(BaseModel):
    id: int
    title: str | None = None
    date: date
    tasks: list[TaskOut]
    steps: list[FocusStepOut | BreakStepOut] = []

    model_config = ConfigDict(from_attributes=True)


class FocusStepCreate(BaseModel):
    sessions_count: int = Field(gt=0, default=1)
