from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.models import User
from app.routers.auth import get_current_user
from app.ai_counsellor import ai_counsellor
import app.crud as crud

router = APIRouter(prefix="/api/counsellor", tags=["AI Counsellor"])

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with AI counsellor
    
    Sends message to AI and gets personalized response based on user profile
    """
    
    # Get user profile for context
    profile = crud.get_user_profile(db, current_user.id)
    
    user_profile_dict = None
    if profile:
        user_profile_dict = {
            "academic_background": profile.academic_background,
            "interests": profile.interests,
            "career_goals": profile.career_goals,
            "preferences": profile.preferences,
            "test_scores": profile.test_scores
        }
    
    # Convert conversation history to format expected by AI
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in request.conversation_history
    ] if request.conversation_history else []
    
    # Get AI response
    response_text = ai_counsellor.chat(
        message=request.message,
        user_profile=user_profile_dict,
        conversation_history=conversation_history
    )
    
    return ChatResponse(response=response_text)

@router.get("/conversations")
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's conversation history"""
    conversations = crud.get_user_conversations(db, current_user.id, limit=20)
    
    return {
        "conversations": [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at
            }
            for conv in conversations
        ]
    }

@router.post("/conversations")
async def create_conversation(
    title: str = "New Conversation",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    conversation = crud.create_conversation(db, current_user.id, title)
    
    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at
    }

@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages from a specific conversation"""
    from uuid import UUID
    
    messages = crud.get_conversation_messages(db, UUID(conversation_id), limit=100)
    
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }

@router.post("/conversations/{conversation_id}/messages")
async def add_message(
    conversation_id: str,
    role: str,
    content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a message to a conversation"""
    from uuid import UUID
    
    message = crud.create_message(db, UUID(conversation_id), role, content)
    
    return {
        "id": str(message.id),
        "conversation_id": conversation_id,
        "role": message.role,
        "content": message.content,
        "created_at": message.created_at
    }
