from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class DifficultyEnum(str, enum.Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

class StatusEnum(str, enum.Enum):
    solved = "Solved"
    unsolved = "Unsolved"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    progresses = relationship("Progress", back_populates="user", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    leetcode_number = Column(Integer, index=True, nullable=True)
    difficulty = Column(Enum(DifficultyEnum), nullable=False)
    topic = Column(String, index=True, nullable=False)
    problem_link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    progresses = relationship("Progress", back_populates="question", cascade="all, delete-orphan")

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.unsolved, nullable=False)
    notes = Column(Text, nullable=True)
    solved_date = Column(DateTime(timezone=True), nullable=True)
    next_revision = Column(Date, nullable=True)

    user = relationship("User", back_populates="progresses")
    question = relationship("Question", back_populates="progresses")
