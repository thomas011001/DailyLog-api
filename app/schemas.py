from datetime import date, datetime

from pydantic import BaseModel, Field, ConfigDict


class CreateUser(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=5)


class UserOut(BaseModel):
    id: int
    username: str

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
    description: str | None = None
    priority: int = 1
    remind_at: datetime | None = None

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

    model_config = ConfigDict(from_attributes=True)


class UpdateDay(BaseModel):
    title: str | None = None
    new_date: date | None = None


class UserTokenData(BaseModel):
    id: int
    username: str


class CreateTask(BaseModel):
    day_id: int
    title: str
    description: str | None = None
    priority: int = 1
    remind_at: datetime | None = None


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = None
    remind_at: datetime | None = None


class CreateNote(BaseModel):
    day_id: int
    content: str


class UpdateNote(BaseModel):
    content: str | None = None

