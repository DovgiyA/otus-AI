"""
SQLAlchemy ORM models for Question, Submission, and Answer entities.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Question(Base):
    """Survey question model."""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)  # "text" or "radio"
    options = Column(JSON, nullable=True)  # For radio questions: ["Option 1", "Option 2", ...]
    order = Column(Integer, default=0)
    
    # Relationships
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Question(id={self.id}, text={self.text}, type={self.type})>"


class Submission(Base):
    """Survey submission model - groups all answers from a participant."""
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    participant_name = Column(String(255), nullable=False)
    participant_email = Column(String(255), nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    answers = relationship("Answer", back_populates="submission", cascade="all, delete-orphan")
    
    # Index for searching and sorting
    __table_args__ = (
        Index('ix_submissions_email_date', 'participant_email', 'submitted_at'),
    )
    
    def __repr__(self):
        return f"<Submission(id={self.id}, name={self.participant_name}, email={self.participant_email})>"


class Answer(Base):
    """User survey answer model."""
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=True)  # Nullable for legacy support
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_value = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    submission = relationship("Submission", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    
    def __repr__(self):
        return f"<Answer(id={self.id}, submission_id={self.submission_id}, question_id={self.question_id})>"
