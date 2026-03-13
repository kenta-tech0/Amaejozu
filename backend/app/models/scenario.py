"""
Scenario model - シナリオマスターデータ
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    title_ja = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    description_ja = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    category = Column(String(30), nullable=False)  # daily, business, travel
    system_prompt = Column(Text, nullable=False)
    first_message = Column(Text, nullable=False)
    icon = Column(String(10), nullable=False, default="💬")
    estimated_turns = Column(Integer, nullable=False, default=8)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    sessions = relationship("PracticeSession", back_populates="scenario")
