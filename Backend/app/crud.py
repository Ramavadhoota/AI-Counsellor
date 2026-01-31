from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List, Dict, Any
from uuid import UUID
import uuid
from app.models import User, UserProfile, Conversation, Message
from app.auth import get_password_hash

# ============================================
# USER CRUD OPERATIONS
# ============================================

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, password: str, full_name: str) -> User:
    """Create new user"""
    hashed_password = get_password_hash(password)
    user = User(
        id=uuid.uuid4(),
        email=email,
        password_hash=hashed_password,
        full_name=full_name,
        onboarding_completed=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_onboarding_status(db: Session, user_id: UUID, completed: bool = True) -> User:
    """Update user onboarding status"""
    user = get_user_by_id(db, user_id)
    if user:
        user.onboarding_completed = completed
        db.commit()
        db.refresh(user)
    return user

# ============================================
# USER PROFILE CRUD OPERATIONS
# ============================================

def get_user_profile(db: Session, user_id: UUID) -> Optional[UserProfile]:
    """Get user profile"""
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

def create_or_update_profile(
    db: Session,
    user_id: UUID,
    academic_background: Optional[Dict[str, Any]] = None,
    interests: Optional[List[str]] = None,
    career_goals: Optional[Dict[str, Any]] = None,
    preferences: Optional[Dict[str, Any]] = None,
    test_scores: Optional[Dict[str, Any]] = None
) -> UserProfile:
    """Create or update user profile"""
    profile = get_user_profile(db, user_id)
    
    if profile:
        # Update existing profile
        if academic_background is not None:
            profile.academic_background = academic_background
        if interests is not None:
            profile.interests = interests
        if career_goals is not None:
            profile.career_goals = career_goals
        if preferences is not None:
            profile.preferences = preferences
        if test_scores is not None:
            profile.test_scores = test_scores
    else:
        # Create new profile
        profile = UserProfile(
            id=uuid.uuid4(),
            user_id=user_id,
            academic_background=academic_background or {},
            interests=interests or [],
            career_goals=career_goals or {},
            preferences=preferences or {},
            test_scores=test_scores
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return profile

# ============================================
# CONVERSATION CRUD OPERATIONS
# ============================================

def create_conversation(db: Session, user_id: UUID, title: str = "New Conversation") -> Conversation:
    """Create new conversation"""
    conversation = Conversation(
        id=uuid.uuid4(),
        user_id=user_id,
        title=title
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversation(db: Session, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
    """Get conversation by ID"""
    return db.query(Conversation).filter(
        and_(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    ).first()

def get_user_conversations(db: Session, user_id: UUID, limit: int = 10) -> List[Conversation]:
    """Get user's recent conversations"""
    return db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(Conversation.updated_at.desc()).limit(limit).all()

def update_conversation_title(db: Session, conversation_id: UUID, title: str) -> Optional[Conversation]:
    """Update conversation title"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation:
        conversation.title = title
        db.commit()
        db.refresh(conversation)
    return conversation

# ============================================
# MESSAGE CRUD OPERATIONS
# ============================================

def create_message(
    db: Session,
    conversation_id: UUID,
    role: str,
    content: str
) -> Message:
    """Create new message in conversation"""
    message = Message(
        id=uuid.uuid4(),
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_conversation_messages(
    db: Session,
    conversation_id: UUID,
    limit: int = 50
) -> List[Message]:
    """Get messages from a conversation"""
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).limit(limit).all()

def delete_conversation(db: Session, conversation_id: UUID, user_id: UUID) -> bool:
    """Delete conversation and all its messages"""
    conversation = get_conversation(db, conversation_id, user_id)
    if conversation:
        # Delete all messages first
        db.query(Message).filter(Message.conversation_id == conversation_id).delete()
        # Delete conversation
        db.delete(conversation)
        db.commit()
        return True
    return False
