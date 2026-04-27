"""
Survey API router with endpoints for questions, answers, and submissions.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from database import get_db, init_db
from models import Question, Answer, Submission
from schemas import (
    QuestionResponse, 
    AnswersRequest, 
    SuccessResponse,
    SubmissionCreateRequest,
    SubmissionListItem,
    SubmissionDetailResponse,
    SubmissionDetailAnswer
)
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
    POST /answers (LEGACY ENDPOINT)
    Accepts and saves user survey answers.
    Expected payload: {"answers": [{"question_id": 1, "answer_value": "text"}, ...]}
    
    NOTE: New submissions should use POST /submissions instead.
    This endpoint is kept for backward compatibility.
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
            
            # Save answer (without submission association for legacy compatibility)
            answer = Answer(
                question_id=answer_data.question_id,
                answer_value=answer_data.answer_value,
                submission_id=None  # Will be NULL for legacy answers
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


# New submission endpoints

@router.post("/submissions", response_model=SuccessResponse)
def create_submission(request: SubmissionCreateRequest, db: Session = Depends(get_db)):
    """
    POST /submissions
    Creates a new submission with participant info and answers.
    Accepts: {"participant_name": "...", "participant_email": "...", "answers": [...]}
    """
    if not request.answers:
        raise HTTPException(status_code=400, detail="No answers provided")
    
    if not request.participant_name.strip():
        raise HTTPException(status_code=400, detail="Participant name required")
    
    if not request.participant_email.strip():
        raise HTTPException(status_code=400, detail="Participant email required")
    
    try:
        # Create submission
        submission = Submission(
            participant_name=request.participant_name.strip(),
            participant_email=request.participant_email.strip()
        )
        db.add(submission)
        db.flush()  # Get the submission ID without committing
        
        # Validate and add answers
        for answer_data in request.answers:
            # Validate question exists
            question = db.query(Question).filter(Question.id == answer_data.question_id).first()
            if not question:
                db.rollback()
                raise HTTPException(
                    status_code=404, 
                    detail=f"Question {answer_data.question_id} not found"
                )
            
            # Create and add answer
            answer = Answer(
                submission_id=submission.id,
                question_id=answer_data.question_id,
                answer_value=answer_data.answer_value.strip()
            )
            db.add(answer)
        
        db.commit()
        
        return SuccessResponse(
            success=True,
            message=f"Successfully saved submission from {request.participant_name}",
            data={"submission_id": submission.id, "answers_count": len(request.answers)}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/submissions", response_model=List[SubmissionListItem])
def list_submissions(
    search: str = Query(None, description="Search by name or email"),
    sort: str = Query("date_desc", description="Sort by: date_asc, date_desc"),
    db: Session = Depends(get_db)
):
    """
    GET /submissions
    Returns list of all submissions with basic info.
    Query params:
      - search: Filter by participant name or email (optional)
      - sort: Sort order (date_asc, date_desc) (default: date_desc)
    """
    query = db.query(Submission)
    
    # Apply search filter
    if search:
        search_param = f"%{search}%"
        query = query.filter(
            or_(
                Submission.participant_name.ilike(search_param),
                Submission.participant_email.ilike(search_param)
            )
        )
    
    # Apply sorting
    if sort == "date_asc":
        query = query.order_by(Submission.submitted_at.asc())
    else:  # Default to date_desc
        query = query.order_by(Submission.submitted_at.desc())
    
    submissions = query.all()
    
    # Map to response model with answer count
    result = [
        SubmissionListItem(
            id=sub.id,
            participant_name=sub.participant_name,
            participant_email=sub.participant_email,
            submitted_at=sub.submitted_at,
            answer_count=len(sub.answers)
        )
        for sub in submissions
    ]
    
    return result


@router.get("/submissions/{submission_id}", response_model=SubmissionDetailResponse)
def get_submission_detail(submission_id: int, db: Session = Depends(get_db)):
    """
    GET /submissions/{submission_id}
    Returns full submission details with all answers and question texts.
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail=f"Submission {submission_id} not found")
    
    # Build answers with question text
    answers_detail = []
    for answer in submission.answers:
        answers_detail.append(
            SubmissionDetailAnswer(
                question_id=answer.question_id,
                question_text=answer.question.text,
                answer_value=answer.answer_value
            )
        )
    
    # Sort answers by question order
    answers_detail.sort(key=lambda x: x.question_id)
    
    return SubmissionDetailResponse(
        id=submission.id,
        participant_name=submission.participant_name,
        participant_email=submission.participant_email,
        submitted_at=submission.submitted_at,
        answers=answers_detail
    )


@router.delete("/submissions/{submission_id}", response_model=SuccessResponse)
def delete_submission(submission_id: int, db: Session = Depends(get_db)):
    """
    DELETE /submissions/{submission_id}
    Deletes a submission and all its associated answers.
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail=f"Submission {submission_id} not found")
    
    try:
        db.delete(submission)
        db.commit()
        
        return SuccessResponse(
            success=True,
            message=f"Successfully deleted submission {submission_id}",
            data={"deleted_submission_id": submission_id}
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
