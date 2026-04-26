"""
Survey API router with endpoints for questions and answers.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Question, Answer
from schemas import QuestionResponse, AnswersRequest, SuccessResponse
from typing import List

router = APIRouter(prefix="/api", tags=["survey"])

# Hardcoded survey questions template (used for seeding DB)
INITIAL_QUESTIONS = [
    {
        "text": "Какое ваше имя?",
        "type": "text",
        "options": None,
        "order": 1
    },
    {
        "text": "Какова ваша должность?",
        "type": "radio",
        "options": ["Developer", "Designer", "Manager", "Other"],
        "order": 2
    },
    {
        "text": "Сколько лет вы работаете в IT?",
        "type": "radio",
        "options": ["< 1 года", "1-3 года", "3-5 лет", "5+ лет"],
        "order": 3
    },
    {
        "text": "Какие языки программирования вы используете?",
        "type": "text",
        "options": None,
        "order": 4
    },
    {
        "text": "Какова ваша основная категория опыта?",
        "type": "radio",
        "options": ["Backend", "Frontend", "Full-Stack", "DevOps", "Data Science"],
        "order": 5
    }
]


def seed_questions(db: Session):
    """Seed initial questions if database is empty."""
    if db.query(Question).count() == 0:
        for q in INITIAL_QUESTIONS:
            question = Question(
                text=q["text"],
                type=q["type"],
                options=q["options"],
                order=q["order"]
            )
            db.add(question)
        db.commit()
        print("✓ Initial questions seeded into database")


@router.get("/questions", response_model=List[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    """
    GET /questions
    Returns list of survey questions ordered by sequence.
    """
    # Seed questions if empty
    seed_questions(db)
    
    questions = db.query(Question).order_by(Question.order).all()
    return questions


@router.post("/answers", response_model=SuccessResponse)
def submit_answers(request: AnswersRequest, db: Session = Depends(get_db)):
    """
    POST /answers
    Accepts and saves user survey answers.
    Expected payload: {"answers": [{"question_id": 1, "answer_value": "text"}, ...]}
    """
    if not request.answers:
        raise HTTPException(status_code=400, detail="No answers provided")
    
    try:
        # Save all answers
        for answer_data in request.answers:
            # Validate question exists
            question = db.query(Question).filter(Question.id == answer_data.question_id).first()
            if not question:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Question {answer_data.question_id} not found"
                )
            
            # Save answer
            answer = Answer(
                question_id=answer_data.question_id,
                answer_value=answer_data.answer_value
            )
            db.add(answer)
        
        db.commit()
        
        return SuccessResponse(
            success=True,
            message=f"Successfully saved {len(request.answers)} answers",
            data={"count": len(request.answers)}
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
