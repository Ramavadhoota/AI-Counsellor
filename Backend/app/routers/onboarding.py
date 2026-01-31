from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user
import app.crud as crud

router = APIRouter(prefix="/api/onboarding", tags=["Onboarding"])

@router.post("/complete")
def complete_onboarding(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Complete user onboarding process
    
    Expected data structure:
    ```json
    {
        "academic_background": {
            "current_education": "Bachelor's",
            "field_of_study": "Computer Science",
            "institution": "XYZ University",
            "graduation_year": 2025
        },
        "interests": ["AI", "Machine Learning", "Data Science"],
        "career_goals": {
            "target_field": "Software Engineering",
            "preferred_location": "USA",
            "timeline": "2 years"
        },
        "preferences": {
            "countries": ["USA", "Canada", "UK"],
            "budget": "moderate",
            "program_type": "Masters"
        },
        "test_scores": {
            "GRE": 320,
            "TOEFL": 110
        }
    }
    ```
    """
    
    # Create or update user profile
    profile = crud.create_or_update_profile(
        db=db,
        user_id=current_user.id,
        academic_background=data.get("academic_background"),
        interests=data.get("interests"),
        career_goals=data.get("career_goals"),
        preferences=data.get("preferences"),
        test_scores=data.get("test_scores")
    )
    
    # Mark onboarding as completed
    crud.update_user_onboarding_status(db, current_user.id, completed=True)
    
    return {
        "message": "Onboarding completed successfully",
        "user_id": str(current_user.id),
        "profile_id": str(profile.id)
    }

@router.get("/status")
def get_onboarding_status(current_user: User = Depends(get_current_user)):
    """Check if user has completed onboarding"""
    return {
        "completed": current_user.onboarding_completed,
        "user_id": str(current_user.id),
        "full_name": current_user.full_name
    }

@router.post("/skip")
def skip_onboarding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Skip onboarding (mark as completed without data)"""
    crud.update_user_onboarding_status(db, current_user.id, completed=True)
    
    return {
        "message": "Onboarding skipped",
        "user_id": str(current_user.id)
    }
