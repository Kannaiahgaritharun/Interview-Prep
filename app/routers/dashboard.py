from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from .. import models, schemas, dependencies

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    # Total questions available in platform
    total_questions = db.query(models.Question).count()
    
    # Progress records for current user
    user_progress_query = db.query(models.Progress).filter(models.Progress.user_id == current_user.id)
    
    # Solved and Unsolved counts
    total_solved = user_progress_query.filter(models.Progress.status == models.StatusEnum.solved).count()
    total_unsolved = total_questions - total_solved # Assuming unsolved is (total - solved)
    
    # Solved by difficulty
    solved_questions_ids = [p.question_id for p in user_progress_query.filter(models.Progress.status == models.StatusEnum.solved).all()]
    
    easy_solved = db.query(models.Question).filter(models.Question.id.in_(solved_questions_ids), models.Question.difficulty == models.DifficultyEnum.easy).count() if solved_questions_ids else 0
    medium_solved = db.query(models.Question).filter(models.Question.id.in_(solved_questions_ids), models.Question.difficulty == models.DifficultyEnum.medium).count() if solved_questions_ids else 0
    hard_solved = db.query(models.Question).filter(models.Question.id.in_(solved_questions_ids), models.Question.difficulty == models.DifficultyEnum.hard).count() if solved_questions_ids else 0
    
    # Topic distribution of solved questions
    topics_query = db.query(
        models.Question.topic, func.count(models.Question.id).label('count')
    ).filter(models.Question.id.in_(solved_questions_ids)).group_by(models.Question.topic).all() if solved_questions_ids else []
    
    questions_by_topic = [{"topic": t[0], "count": t[1]} for t in topics_query]
    
    # Revision due today
    today = date.today()
    revision_due_today = user_progress_query.filter(models.Progress.next_revision <= today).count()
    
    # Completion percentage
    completion_percentage = (total_solved / total_questions * 100) if total_questions > 0 else 0.0
    
    return {
        "total_questions": total_questions,
        "total_solved": total_solved,
        "total_unsolved": total_unsolved,
        "easy_solved": easy_solved,
        "medium_solved": medium_solved,
        "hard_solved": hard_solved,
        "questions_by_topic": questions_by_topic,
        "revision_due_today": revision_due_today,
        "completion_percentage": round(completion_percentage, 2)
    }
