"""
Message model - 会話メッセージ
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("practice_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    correction = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    turn_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    session = relationship("PracticeSession", back_populates="messages")
