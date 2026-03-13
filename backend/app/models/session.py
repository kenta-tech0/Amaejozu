"""
PracticeSession model - 練習セッション
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class PracticeSession(Base):
    __tablename__ = "practice_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    started_at = Column(DateTime, server_default=func.now())
    ended_at = Column(DateTime, nullable=True)
    total_turns = Column(Integer, default=0)
    score = Column(Integer, nullable=True)
    feedback_summary = Column(Text, nullable=True)
    status = Column(String(20), default="active")  # active, completed, abandoned

    # Relationships
    scenario = relationship("Scenario", back_populates="sessions")
    messages = relationship("Message", back_populates="session", order_by="Message.turn_number")
