from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from .models import DifficultyEnum, StatusEnum

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Question Schemas ---
class QuestionBase(BaseModel):
    title: str
    leetcode_number: Optional[int] = None
    difficulty: DifficultyEnum
    topic: str
    problem_link: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Progress Schemas ---
class ProgressBase(BaseModel):
    status: StatusEnum
    notes: Optional[str] = None
    solved_date: Optional[datetime] = None
    next_revision: Optional[date] = None

class ProgressCreate(ProgressBase):
    question_id: int

class ProgressUpdate(ProgressBase):
    pass

class ProgressOut(ProgressBase):
    id: int
    user_id: int
    question_id: int

    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Dashboard Schemas ---
class TopicCount(BaseModel):
    topic: str
    count: int

class DashboardStats(BaseModel):
    total_questions: int
    total_solved: int
    total_unsolved: int
    easy_solved: int
    medium_solved: int
    hard_solved: int
    questions_by_topic: List[TopicCount]
    revision_due_today: int
    completion_percentage: float
