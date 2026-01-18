"""SQLAlchemy models for HCP interactions."""
from sqlalchemy import Column, Integer, String, Date, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database.db import Base
from datetime import datetime
import enum


class SentimentEnum(str, enum.Enum):
    """Sentiment enumeration for interactions."""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


class Interaction(Base):
    """
    Interaction model representing a meeting with Healthcare Professional.
    
    Fields:
    - hcp_name: Doctor/HCP name (required)
    - date: Meeting date (required)
    - sentiment: Positive/Negative/Neutral (default: Neutral)
    - materials_shared: List of materials (brochures, samples, etc.)
    - discussion_summary: What was discussed
    - products_discussed: List of products mentioned
    - follow_up_date: Optional next meeting date
    - key_insights: Optional AI-generated insights
    - created_at: Auto-set timestamp
    - updated_at: Auto-updated timestamp
    """
    
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), nullable=False, index=True)
    date = Column(Date, nullable=False)
    sentiment = Column(SQLEnum(SentimentEnum), default=SentimentEnum.NEUTRAL)
    materials_shared = Column(JSON, default=list)  # Stores as JSON array
    discussion_summary = Column(String(2000))
    products_discussed = Column(JSON, default=list)  # Stores as JSON array
    follow_up_date = Column(Date, nullable=True)
    key_insights = Column(String(2000), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'hcp_name': self.hcp_name,
            'date': str(self.date) if self.date else None,
            'sentiment': self.sentiment.value if self.sentiment else None,
            'materials_shared': self.materials_shared or [],
            'discussion_summary': self.discussion_summary,
            'products_discussed': self.products_discussed or [],
            'follow_up_date': str(self.follow_up_date) if self.follow_up_date else None,
            'key_insights': self.key_insights,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Interaction(id={self.id}, hcp_name='{self.hcp_name}', date='{self.date}')>"
