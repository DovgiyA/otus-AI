"""
SQLAlchemy ORM models for Question and Answer entities.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
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


class Answer(Base):
    """User survey answer model."""
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_value = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    question = relationship("Question", back_populates="answers")
    
    def __repr__(self):
        return f"<Answer(id={self.id}, question_id={self.question_id}, answer={self.answer_value})>"
