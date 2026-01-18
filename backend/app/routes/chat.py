"""
API routes for HCP interaction management.
Connects FastAPI endpoints with LangGraph agent.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date

from app.database.db import get_db
from app.models.interaction import Interaction, SentimentEnum
from app.schemas.interaction_schema import (
    ChatRequest,
    ChatResponse,
    InteractionCreate,
    InteractionUpdate,
    InteractionResponse
)
from app.agents.hcp_agent import agent

router = APIRouter(prefix="/api", tags=["chat"])


# ============================================================================
# MAIN CHAT ENDPOINT (Uses LangGraph Agent)
# ============================================================================

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint that processes natural language using LangGraph agent.
    
    Flow:
    1. If interaction_id provided, load from DB
    2. Pass user message + current data to agent
    3. Agent returns updated form_data + friendly response
    4. Return to frontend
    
    Args:
        request: ChatRequest with message and optional interaction_id
        db: Database session
    
    Returns:
        ChatResponse with form_data and chat_response
    """
    try:
        # Load existing interaction if ID provided
        current_form_data = None
        if request.interaction_id:
            interaction = db.query(Interaction).filter(
                Interaction.id == request.interaction_id
            ).first()
            
            if not interaction:
                raise HTTPException(status_code=404, detail="Interaction not found")
            
            current_form_data = interaction.to_dict()
        
        # Process with LangGraph agent
        result = agent.process(
            user_input=request.message,
            current_form_data=current_form_data
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=f"Agent processing failed: {result.get('chat_response', 'Unknown error')}"
            )
        
        # Return response
        return ChatResponse(
            form_data=result["form_data"],
            chat_response=result["chat_response"],
            interaction_id=request.interaction_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CRUD ENDPOINTS FOR INTERACTIONS
# ============================================================================

@router.post("/interactions", response_model=InteractionResponse, status_code=201)
async def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    """
    Create a new interaction in the database.
    
    This endpoint is called when user clicks "Save Interaction" button.
    
    Args:
        interaction: InteractionCreate schema with all fields
        db: Database session
    
    Returns:
        Created interaction with ID
    """
    try:
        # Convert sentiment string to enum
        sentiment_enum = SentimentEnum.POSITIVE
        if interaction.sentiment.lower() == "negative":
            sentiment_enum = SentimentEnum.NEGATIVE
        elif interaction.sentiment.lower() == "neutral":
            sentiment_enum = SentimentEnum.NEUTRAL
        
        # Create database model
        db_interaction = Interaction(
            hcp_name=interaction.hcp_name,
            date=interaction.date,
            sentiment=sentiment_enum,
            materials_shared=interaction.materials_shared,
            discussion_summary=interaction.discussion_summary,
            products_discussed=interaction.products_discussed,
            follow_up_date=interaction.follow_up_date,
            key_insights=interaction.key_insights
        )
        
        db.add(db_interaction)
        db.commit()
        db.refresh(db_interaction)
        
        print(f"✅ Created interaction #{db_interaction.id} for {db_interaction.hcp_name}")
        
        return db_interaction
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating interaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/interactions/{interaction_id}", response_model=InteractionResponse)
async def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """
    Get a single interaction by ID.
    
    Args:
        interaction_id: The interaction ID
        db: Database session
    
    Returns:
        Interaction data
    """
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    return interaction


@router.patch("/interactions/{interaction_id}", response_model=InteractionResponse)
async def update_interaction(
    interaction_id: int,
    update_data: InteractionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing interaction (partial update supported).
    
    Args:
        interaction_id: The interaction ID
        update_data: Fields to update (all optional)
        db: Database session
    
    Returns:
        Updated interaction
    """
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    try:
        # Update only provided fields
        update_dict = update_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            if field == "sentiment" and value:
                # Convert sentiment to enum
                if value.lower() == "positive":
                    value = SentimentEnum.POSITIVE
                elif value.lower() == "negative":
                    value = SentimentEnum.NEGATIVE
                else:
                    value = SentimentEnum.NEUTRAL
            
            setattr(interaction, field, value)
        
        db.commit()
        db.refresh(interaction)
        
        print(f"✅ Updated interaction #{interaction_id}")
        
        return interaction
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating interaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/interactions", response_model=List[InteractionResponse])
async def list_interactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all interactions with pagination.
    
    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum records to return (default: 100)
        db: Database session
    
    Returns:
        List of interactions
    """
    interactions = db.query(Interaction).order_by(
        Interaction.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return interactions


@router.delete("/interactions/{interaction_id}")
async def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """
    Delete an interaction.
    
    Args:
        interaction_id: The interaction ID
        db: Database session
    
    Returns:
        Success message
    """
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    try:
        db.delete(interaction)
        db.commit()
        
        print(f"✅ Deleted interaction #{interaction_id}")
        
        return {"message": f"Interaction {interaction_id} deleted successfully"}
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error deleting interaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@router.get("/test")
async def test_route():
    """Test route to verify router is working."""
    return {
        "message": "Chat router is fully operational! 🚀",
        "endpoints": {
            "POST /api/chat": "Main chat endpoint (uses LangGraph agent)",
            "POST /api/interactions": "Create interaction",
            "GET /api/interactions/{id}": "Get single interaction",
            "PATCH /api/interactions/{id}": "Update interaction",
            "GET /api/interactions": "List all interactions",
            "DELETE /api/interactions/{id}": "Delete interaction"
        }
    }
