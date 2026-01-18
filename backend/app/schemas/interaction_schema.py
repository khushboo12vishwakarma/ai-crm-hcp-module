"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional, Any
from datetime import date as date_type, datetime


class InteractionBase(BaseModel):
    """Base schema with common fields."""
    hcp_name: str
    date: date_type
    sentiment: str = "Neutral"
    materials_shared: List[str] = []
    discussion_summary: Optional[str] = None
    products_discussed: List[str] = []
    follow_up_date: Optional[date_type] = None
    key_insights: Optional[str] = None
    
    @field_validator('hcp_name')
    @classmethod
    def validate_hcp_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('HCP name cannot be empty')
        return v


class InteractionCreate(InteractionBase):
    """Schema for creating new interaction."""
    pass


class InteractionUpdate(BaseModel):
    """Schema for updating interaction (all fields optional)."""
    hcp_name: Optional[str] = None
    date: Optional[date_type] = None
    sentiment: Optional[str] = None
    materials_shared: Optional[List[str]] = None
    discussion_summary: Optional[str] = None
    products_discussed: Optional[List[str]] = None
    follow_up_date: Optional[date_type] = None
    key_insights: Optional[str] = None
    
    @field_validator('hcp_name')
    @classmethod
    def validate_hcp_name(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('HCP name cannot be empty')
        return v


class InteractionResponse(InteractionBase):
    """Schema for API response."""
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @model_validator(mode='before')
    @classmethod
    def convert_datetime_fields(cls, data: Any) -> Any:
        """Convert datetime objects to ISO format strings."""
        if hasattr(data, '__dict__'):
            # It's a SQLAlchemy model
            obj = data
            return {
                'id': obj.id,
                'hcp_name': obj.hcp_name,
                'date': obj.date,
                'sentiment': obj.sentiment.value if hasattr(obj.sentiment, 'value') else str(obj.sentiment),
                'materials_shared': obj.materials_shared or [],
                'discussion_summary': obj.discussion_summary,
                'products_discussed': obj.products_discussed or [],
                'follow_up_date': obj.follow_up_date,
                'key_insights': obj.key_insights,
                'created_at': obj.created_at.isoformat() if obj.created_at else None,
                'updated_at': obj.updated_at.isoformat() if obj.updated_at else None
            }
        return data
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """Schema for chat request."""
    message: str
    interaction_id: Optional[int] = None
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Message cannot be empty')
        return v


class ChatResponse(BaseModel):
    """Schema for chat response."""
    form_data: dict
    chat_response: str
    interaction_id: Optional[int] = None
