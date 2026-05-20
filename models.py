from sqlalchemy import Column, Integer, String , ForeignKey , DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, UTC


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="pending")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
 
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    updated_at = Column(
    DateTime,
    default=lambda: datetime.now(UTC),
    onupdate=lambda: datetime.now(UTC)
    )
    owner = relationship("User", back_populates="tasks")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    tasks = relationship("Task", back_populates="owner")