import datetime
import os

from dotenv import load_dotenv
import jwt
from sqlalchemy import (
    Column,
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
from sqlalchemy.orm import relationship
from app.core.db import Base

load_dotenv()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    days = relationship("Day", back_populates="owner", cascade="all, delete-orphan")

    @property
    def token(self):
        payload = {
            "id": self.id,
            "username": self.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=48),
        }
        token = jwt.encode(payload, os.getenv("ACCESS_TOKEN_KEY", "very secret key"))
        return token


class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    date = Column(Date, nullable=False, index=True)
    # daily_summary = Column(Text)
    title = Column(String, nullable=True)

    owner = relationship("User", back_populates="days")
    tasks = relationship("Task", back_populates="day", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="day", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("user_id", "date", name="_user_day_uc"),)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="pending", index=True)
    priority = Column(Integer, default=1, index=True)
    remind_at = Column(DateTime, index=True)
    is_notified = Column(Boolean, default=False)

    day = relationship("Day", back_populates="tasks")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    day = relationship("Day", back_populates="notes")
