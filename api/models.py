import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    refresh_token = Column(Text)

    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )

    tasks = relationship("Task")


class TaskStatus(str, enum.Enum):
    Yet = "YET"
    Doing = "DOING"
    Done = "DONE"


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.Yet)

    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )

    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="tasks")
