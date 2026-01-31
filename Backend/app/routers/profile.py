from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.schemas import ProfileData
from app.models import User
from app.routers.auth import get_current_user
import app.crud as crud

router = APIRouter(prefix="/api/profile", tags=["User Profile"])

@router.get("/")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile with all details"""
    profile = crud.get_user_profile(db, current_user.id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please complete onboarding first."
        )
    
    return {
        "user_id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "onboarding_completed": current_user.onboarding_completed,
        "academic_background": profile.academic_background,
        "interests": profile.interests,
        "career_goals": profile.career_goals,
        "preferences": profile.preferences,
        "test_scores": profile.test_scores,
        "created_at": profile.created_at,
        "updated_at": profile.updated_at
    }

@router.put("/")
def update_profile(
    data: ProfileData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile
    
    Only updates fields that are provided (partial update)
    """
    profile = crud.create_or_update_profile(
        db=db,
        user_id=current_user.id,
        academic_background=data.academic_background,
        interests=data.interests,
        career_goals=data.career_goals,
        preferences=data.preferences,
        test_scores=data.test_scores
    )
    
    return {
        "message": "Profile updated successfully",
        "user_id": str(current_user.id),
        "profile_id": str(profile.id)
    }

@router.delete("/")
def delete_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user profile data (keeps user account)"""
    profile = crud.get_user_profile(db, current_user.id)
    
    if profile:
        db.delete(profile)
        db.commit()
    
    # Mark onboarding as incomplete
    crud.update_user_onboarding_status(db, current_user.id, completed=False)
    
    return {
        "message": "Profile deleted successfully",
        "user_id": str(current_user.id)
    }
