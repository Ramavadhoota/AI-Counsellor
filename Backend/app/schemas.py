from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# ============================================
# USER SCHEMAS
# ============================================

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: UUID
    onboarding_completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

# ============================================
# ONBOARDING SCHEMAS
# ============================================

class OnboardingData(BaseModel):
    academic_background: Dict[str, Any] = Field(
        ..., 
        description="Academic info: current_education, field_of_study, grades, institution"
    )
    interests: List[str] = Field(..., description="List of subjects/fields of interest")
    career_goals: Dict[str, Any] = Field(
        ...,
        description="Career aspirations: target_field, preferred_location, timeline"
    )
    preferences: Dict[str, Any] = Field(
        ...,
        description="Study preferences: location, budget, program_type, duration"
    )
    test_scores: Optional[Dict[str, Any]] = Field(
        None,
        description="Standardized test scores if applicable"
    )

class OnboardingResponse(BaseModel):
    message: str
    user_id: UUID

# ============================================
# PROFILE SCHEMAS
# ============================================

class ProfileData(BaseModel):
    academic_background: Optional[Dict[str, Any]] = None
    interests: Optional[List[str]] = None
    career_goals: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None
    test_scores: Optional[Dict[str, Any]] = None

class ProfileResponse(ProfileData):
    user_id: UUID
    full_name: str
    email: str
    
    class Config:
        from_attributes = True

# ============================================
# CHAT SCHEMAS
# ============================================

class ChatMessage(BaseModel):
    role: str = Field(..., description="Either 'user' or 'assistant'")
    content: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_history: Optional[List[ChatMessage]] = Field(default_factory=list)

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[UUID] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================
# UNIVERSITY RECOMMENDATION SCHEMAS
# ============================================

class UniversitySearchParams(BaseModel):
    country: Optional[str] = None
    name_query: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)

class University(BaseModel):
    name: str
    country: str
    web_pages: List[str]
    domains: List[str]
    alpha_two_code: str
    state_province: Optional[str] = None

class UniversityRecommendationRequest(BaseModel):
    preferences: Optional[Dict[str, Any]] = None
    limit: int = Field(default=5, ge=1, le=20)

class UniversityRecommendation(BaseModel):
    university: University
    match_score: float = Field(..., ge=0, le=100)
    reasoning: str

class UniversityRecommendationResponse(BaseModel):
    recommendations: List[UniversityRecommendation]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================
# CAREER PATH SCHEMAS
# ============================================

class CareerPathRequest(BaseModel):
    field_of_interest: Optional[str] = None
    
class CareerOption(BaseModel):
    career_title: str
    description: str
    required_education: List[str]
    average_salary_range: str
    growth_outlook: str
    key_skills: List[str]

class CareerPathResponse(BaseModel):
    career_options: List[CareerOption]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================
# COURSE RECOMMENDATION SCHEMAS
# ============================================

class CourseRecommendationRequest(BaseModel):
    career_goal: Optional[str] = None
    current_level: Optional[str] = None

class CourseRecommendation(BaseModel):
    course_name: str
    institution_type: str
    duration: str
    description: str
    prerequisites: List[str]
    career_outcomes: List[str]

class CourseRecommendationResponse(BaseModel):
    recommendations: List[CourseRecommendation]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================
# DOCUMENT ANALYSIS SCHEMAS
# ============================================

class DocumentAnalysisResponse(BaseModel):
    analysis: str
    suggestions: List[str]
    strengths: List[str]
    improvements: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================
# ERROR SCHEMAS
# ============================================

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
