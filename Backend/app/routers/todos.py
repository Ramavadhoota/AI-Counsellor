from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
import uuid

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/todos", tags=["Todos"])

# Simple in-memory storage (for demo purposes)
# In production, create a Todo model in models.py
todos_db = {}

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"  # low, medium, high
    category: str = "general"  # academic, career, application, general

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    category: Optional[str] = None

class TodoResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    category: str
    created_at: datetime
    updated_at: datetime

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new todo item"""
    todo_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    new_todo = {
        "id": todo_id,
        "user_id": str(current_user.id),
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "priority": todo.priority,
        "category": todo.category,
        "created_at": now,
        "updated_at": now
    }
    
    if str(current_user.id) not in todos_db:
        todos_db[str(current_user.id)] = {}
    
    todos_db[str(current_user.id)][todo_id] = new_todo
    
    return new_todo

@router.get("/", response_model=List[TodoResponse])
def get_todos(
    category: Optional[str] = None,
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user)
):
    """Get all todos for current user with optional filters"""
    user_id = str(current_user.id)
    
    if user_id not in todos_db:
        return []
    
    user_todos = list(todos_db[user_id].values())
    
    # Apply filters
    if category:
        user_todos = [t for t in user_todos if t["category"] == category]
    
    if completed is not None:
        user_todos = [t for t in user_todos if t["completed"] == completed]
    
    # Sort by created_at descending
    user_todos.sort(key=lambda x: x["created_at"], reverse=True)
    
    return user_todos

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific todo by ID"""
    user_id = str(current_user.id)
    
    if user_id not in todos_db or todo_id not in todos_db[user_id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return todos_db[user_id][todo_id]

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a todo item"""
    user_id = str(current_user.id)
    
    if user_id not in todos_db or todo_id not in todos_db[user_id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    todo = todos_db[user_id][todo_id]
    
    # Update fields if provided
    if todo_update.title is not None:
        todo["title"] = todo_update.title
    if todo_update.description is not None:
        todo["description"] = todo_update.description
    if todo_update.completed is not None:
        todo["completed"] = todo_update.completed
    if todo_update.priority is not None:
        todo["priority"] = todo_update.priority
    if todo_update.category is not None:
        todo["category"] = todo_update.category
    
    todo["updated_at"] = datetime.utcnow()
    
    return todo

@router.delete("/{todo_id}")
def delete_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a todo item"""
    user_id = str(current_user.id)
    
    if user_id not in todos_db or todo_id not in todos_db[user_id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    del todos_db[user_id][todo_id]
    
    return {"message": "Todo deleted successfully", "todo_id": todo_id}

@router.post("/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo(
    todo_id: str,
    current_user: User = Depends(get_current_user)
):
    """Toggle todo completion status"""
    user_id = str(current_user.id)
    
    if user_id not in todos_db or todo_id not in todos_db[user_id]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    todo = todos_db[user_id][todo_id]
    todo["completed"] = not todo["completed"]
    todo["updated_at"] = datetime.utcnow()
    
    return todo
