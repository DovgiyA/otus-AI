"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class QuestionResponse(BaseModel):
    """Response schema for a survey question."""
    id: int
    text: str
    type: str  # "text" or "radio"
    options: Optional[List[str]] = None
    order: int
    
    class Config:
        from_attributes = True


class AnswerSubmit(BaseModel):
    """Schema for a single answer submission."""
    question_id: int
    answer_value: str


class AnswersRequest(BaseModel):
    """Request schema for submitting multiple answers (legacy)."""
    answers: List[AnswerSubmit]


class AnswerResponse(BaseModel):
    """Response schema for a saved answer."""
    id: int
    question_id: int
    answer_value: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class SuccessResponse(BaseModel):
    """Generic success response."""
    success: bool
    message: str
    data: Optional[dict] = None


# New schemas for Submission

class SubmissionAnswerSubmit(BaseModel):
    """Schema for a single answer in submission."""
    question_id: int
    answer_value: str


class SubmissionCreateRequest(BaseModel):
    """Request schema for creating a new submission with answers."""
    participant_name: str
    participant_email: str
    answers: List[SubmissionAnswerSubmit]


class SubmissionListItem(BaseModel):
    """Response schema for submission in list view."""
    id: int
    participant_name: str
    participant_email: str
    submitted_at: datetime
    answer_count: int
    
    class Config:
        from_attributes = True


class SubmissionDetailAnswer(BaseModel):
    """Answer details in submission detail view."""
    question_id: int
    question_text: str
    answer_value: str


class SubmissionDetailResponse(BaseModel):
    """Response schema for detailed submission view."""
    id: int
    participant_name: str
    participant_email: str
    submitted_at: datetime
    answers: List[SubmissionDetailAnswer]
    
    class Config:
        from_attributes = True
