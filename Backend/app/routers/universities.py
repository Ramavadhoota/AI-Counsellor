from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user
from app.university_service import university_service
import app.crud as crud

router = APIRouter(prefix="/api/universities", tags=["Universities"])

@router.get("/search")
async def search_universities(
    country: str = None,
    name: str = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """
    Search universities by country and/or name
    
    - **country**: Country name (e.g., "United States", "India")
    - **name**: University name search query
    - **limit**: Maximum number of results (default: 10)
    """
    
    universities = await university_service.search_universities(
        country=country,
        name=name
    )
    
    # Format and limit results
    formatted = [
        university_service.format_university_data(uni)
        for uni in universities[:limit]
    ]
    
    return {
        "count": len(formatted),
        "universities": formatted
    }

@router.get("/countries")
async def get_countries(current_user: User = Depends(get_current_user)):
    """Get list of popular study destination countries"""
    countries = [
        {"code": "US", "name": "United States"},
        {"code": "GB", "name": "United Kingdom"},
        {"code": "CA", "name": "Canada"},
        {"code": "AU", "name": "Australia"},
        {"code": "DE", "name": "Germany"},
        {"code": "FR", "name": "France"},
        {"code": "NL", "name": "Netherlands"},
        {"code": "SE", "name": "Sweden"},
        {"code": "CH", "name": "Switzerland"},
        {"code": "SG", "name": "Singapore"},
        {"code": "JP", "name": "Japan"},
        {"code": "KR", "name": "South Korea"},
        {"code": "NZ", "name": "New Zealand"},
        {"code": "IE", "name": "Ireland"},
        {"code": "IN", "name": "India"}
    ]
    return {"countries": countries}

@router.get("/recommendations")
async def get_recommendations(
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized university recommendations based on user profile
    """
    
    # Get user profile
    profile = crud.get_user_profile(db, current_user.id)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please complete onboarding first to get recommendations"
        )
    
    # Get preferred countries from profile
    preferences = profile.preferences or {}
    preferred_countries = preferences.get("countries", ["United States", "United Kingdom", "Canada"])
    
    # Fetch universities from preferred countries
    all_universities = []
    for country in preferred_countries[:3]:  # Limit to 3 countries
        universities = await university_service.search_universities(country=country)
        all_universities.extend(universities[:10])  # 10 per country
    
    if not all_universities:
        return {
            "count": 0,
            "recommendations": [],
            "message": "No universities found for your preferred countries"
        }
    
    # Format results
    formatted = [
        university_service.format_university_data(uni)
        for uni in all_universities[:limit]
    ]
    
    return {
        "count": len(formatted),
        "recommendations": formatted,
        "based_on": {
            "countries": preferred_countries,
            "interests": profile.interests,
            "career_goals": profile.career_goals
        }
    }

@router.get("/{country}")
async def get_universities_by_country(
    country: str,
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """Get all universities in a specific country"""
    
    universities = await university_service.search_universities(country=country)
    
    formatted = [
        university_service.format_university_data(uni)
        for uni in universities[:limit]
    ]
    
    return {
        "country": country,
        "count": len(formatted),
        "universities": formatted
    }
