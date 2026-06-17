from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, dependencies

router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.post("/", response_model=schemas.QuestionOut)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    new_question = models.Question(**question.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@router.get("/", response_model=List[schemas.QuestionOut])
def get_questions(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user_optional),
    topic: Optional[str] = None,
    difficulty: Optional[models.DifficultyEnum] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Question)
    if topic:
        query = query.filter(models.Question.topic == topic)
    if difficulty:
        query = query.filter(models.Question.difficulty == difficulty)
    if search:
        query = query.filter(models.Question.title.ilike(f"%{search}%"))
        
    questions = query.offset(skip).limit(limit).all()
    return questions

@router.get("/{id}", response_model=schemas.QuestionOut)
def get_question(id: int, db: Session = Depends(dependencies.get_db)):
    question = db.query(models.Question).filter(models.Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{id}", response_model=schemas.QuestionOut)
def update_question(id: int, updated_question: schemas.QuestionCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    question_query = db.query(models.Question).filter(models.Question.id == id)
    question = question_query.first()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    question_query.update(updated_question.dict(), synchronize_session=False)
    db.commit()
    return question_query.first()

@router.delete("/{id}")
def delete_question(id: int, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    question_query = db.query(models.Question).filter(models.Question.id == id)
    if not question_query.first():
        raise HTTPException(status_code=404, detail="Question not found")
        
    question_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Question deleted"}
