import datetime
import os
from typing import Optional

from dotenv import load_dotenv
import jwt
from sqlalchemy import (
    Column,
    Enum,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Date,
    Boolean,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

from .schemas import StepType

load_dotenv()

# Mars 3 2025 - DayTitle - Target: 16 --> Day Model --> User Model
# ----------------------
# [ ] Task One                        --> Task Model --> Day Model
# [ ] Task Two
# [ ] Task Three
# ----------------------
# 1. O (O: Focus Session)             --> Focus Session Model --> Focus Step Model --> Day Model
# 2. coffee break                     --> Break Step Model --> Day Model
# 3. O O O
# 4. 30m Scrolling
# 5. O O O O


class User(Base):
    __tablename__ = "users"

    # old version

    # id = Column(Integer, primary_key=True, index=True)
    # first_name = Column(String(100), nullable=True)
    # last_name = Column(String(100), nullable=True)
    # username = Column(String(50), unique=True, nullable=False, index=True)
    # password_hash = Column(Text, nullable=False)
    # created_at = Column(DateTime, server_default=func.now())

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    days: Mapped[list["Day"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    @property
    def token(self):
        payload = {
            "id": self.id,
            "username": self.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=48),
        }
        token = jwt.encode(payload, os.getenv("ACCESS_TOKEN_KEY", "very secret key"))
        return token

    @property
    def auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"}


class Day(Base):
    __tablename__ = "days"

    # old version

    # id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(
    #     Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    # )
    # date = Column(Date, nullable=False, index=True)
    # title = Column(String, nullable=True)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[datetime.date]
    title: Mapped[Optional[str]]

    owner: Mapped["User"] = relationship(back_populates="days")
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="day", cascade="all, delete-orphan"
    )
    steps: Mapped[list["BaseStep"]] = relationship(
        back_populates="day",
        cascade="all, delete-orphan",
        order_by="BaseStep.order",
    )

    # will be deleted
    notes: Mapped[list["Note"]] = relationship(
        back_populates="day", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("user_id", "date", name="_user_day_uc"),)


class Task(Base):
    __tablename__ = "tasks"

    # id = Column(Integer, primary_key=True, index=True)
    # day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    # title = Column(String(255), nullable=False)
    # status = Column(String(20), default="pending", index=True)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    day_id: Mapped[int] = mapped_column(ForeignKey("days.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(default="pending")

    day: Mapped["Day"] = relationship(back_populates="tasks")

    # will be deleted
    description = Column(Text)


# will be deleted
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    day = relationship("Day", back_populates="notes")


class FocusSession(Base):
    __tablename__ = "focus_sessions"

    # old version

    # id = Column(Integer, primary_key=True)
    # focus_step_id = Column(Integer, ForeignKey("focus_step.id", ondelete="CASCADE"))
    # is_completed = Column(Boolean, default=False)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    focus_step_id: Mapped[int] = mapped_column(
        ForeignKey("focus_step.id", ondelete="CASCADE")
    )
    is_completed: Mapped[bool] = mapped_column(default=False)

    step: Mapped["FocusStep"] = relationship(back_populates="sessions")


class BaseStep(Base):
    __tablename__ = "base_step"

    # old version

    # id = Column(Integer, primary_key=True, index=True)
    # order = Column(Integer, nullable=False)
    # day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    # type_identity = Column(String(50))
    # is_completed = Column(Boolean, default=False)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order: Mapped[int]
    day_id: Mapped[int] = mapped_column(ForeignKey("days.id", ondelete="CASCADE"))
    type_identity: Mapped[str] = mapped_column(String(50))
    is_completed: Mapped[bool] = mapped_column(default=False)

    __mapper_args__ = {
        "polymorphic_identity": "base",
        "polymorphic_on": "type_identity",
    }

    day: Mapped["Day"] = relationship("Day", back_populates="steps")

    __table_args__ = (UniqueConstraint("day_id", "order", name="_day_order_uc"),)


class FocusStep(BaseStep):
    __tablename__ = "focus_step"

    # old version

    # id = Column(
    #     Integer, ForeignKey("base_step.id", ondelete="CASCADE"), primary_key=True
    # )
    # sessions_count = Column(Integer, default=1)

    id: Mapped[int] = mapped_column(
        ForeignKey("base_step.id", ondelete="CASCADE"), primary_key=True
    )

    sessions_count: Mapped[int] = mapped_column(default=1)

    sessions: Mapped[list["FocusSession"]] = relationship(
        back_populates="step", cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "focus",
    }


class BreakStep(BaseStep):
    __tablename__ = "break_steps"

    id: Mapped[int] = mapped_column(
        ForeignKey("base_step.id", ondelete="CASCADE"), primary_key=True
    )

    description: Mapped[Optional[str]] = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_identity": "break",
    }
