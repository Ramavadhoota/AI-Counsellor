from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from uuid import UUID

from app.database import get_db
from app.schemas import UserCreate, UserLogin, UserResponse, Token, TokenData
from app.models import User
from app.auth import verify_password, create_access_token
from app.config import settings
import app.crud as crud

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()

# ============================================
# DEPENDENCY: Get Current User
# ============================================

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_id(db, UUID(token_data.user_id))
    if user is None:
        raise credentials_exception
    
    return user

# ============================================
# AUTH ENDPOINTS
# ============================================

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Password (min 6 characters)
    - **full_name**: User's full name
    """
    # Check if user already exists
    existing_user = crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = crud.create_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return Token(access_token=access_token, token_type="bearer")

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user with email and password
    
    Returns JWT access token
    """
    user = crud.get_user_by_email(db, credentials.email)
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return current_user

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user
    
    Note: Client should discard the JWT token
    """
    return {"message": "Successfully logged out", "user_id": str(current_user.id)}

@router.post("/refresh", response_model=Token)
def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh JWT access token"""
    access_token = create_access_token(data={"sub": str(current_user.id)})
    return Token(access_token=access_token, token_type="bearer")
