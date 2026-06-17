from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .. import models, schemas, dependencies

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.post("/", response_model=schemas.ProgressOut)
def log_progress(progress: schemas.ProgressCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    # Check if question exists
    question = db.query(models.Question).filter(models.Question.id == progress.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    # Check if progress already exists for this user and question
    existing_progress = db.query(models.Progress).filter(
        models.Progress.user_id == current_user.id,
        models.Progress.question_id == progress.question_id
    ).first()
    
    if existing_progress:
        # Update existing
        for key, value in progress.dict().items():
            setattr(existing_progress, key, value)
        if progress.status == models.StatusEnum.solved and not existing_progress.solved_date:
            existing_progress.solved_date = datetime.utcnow()
        db.commit()
        db.refresh(existing_progress)
        return existing_progress
    else:
        # Create new
        new_progress = models.Progress(**progress.dict(), user_id=current_user.id)
        if progress.status == models.StatusEnum.solved:
            new_progress.solved_date = datetime.utcnow()
        db.add(new_progress)
        db.commit()
        db.refresh(new_progress)
        return new_progress

@router.get("/", response_model=List[schemas.ProgressOut])
def get_user_progress(db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    progress_records = db.query(models.Progress).filter(models.Progress.user_id == current_user.id).all()
    return progress_records

@router.get("/{question_id}", response_model=schemas.ProgressOut)
def get_question_progress(question_id: int, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    progress = db.query(models.Progress).filter(
        models.Progress.user_id == current_user.id,
        models.Progress.question_id == question_id
    ).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found for this question")
    return progress
