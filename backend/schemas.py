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
    """Request schema for submitting multiple answers."""
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
