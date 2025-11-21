from fastapi import APIRouter, HTTPException, status, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set. Please set it to a secure value.")
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_current_user_id(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return "authenticated_user"
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "Bearer"},
    )

todos_db: Dict[int, Dict[str, any]] = {}
next_todo_id: int = 1

router = APIRouter()

class TodoBase(BaseModel):
    title: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None

class TodoInDB(TodoBase):
    id: int
    completed: bool = False
    owner: str

def get_todo_or_404_and_authorize(todo_id: int, current_user: str):
    if todo_id not in todos_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    
    todo = todos_db[todo_id]
    if todo["owner"] != current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    
    return todo

@router.get("/todos", response_model=List[TodoInDB])
async def read_all_todos(current_user: str = Depends(get_current_user_id)):
    user_todos = [TodoInDB(**todo) for todo_id, todo in todos_db.items() if todo["owner"] == current_user]
    return user_todos

@router.get("/todos/{todo_id}", response_model=TodoInDB)
async def read_todo(todo_id: int, current_user: str = Depends(get_current_user_id)):
    todo = get_todo_or_404_and_authorize(todo_id, current_user)
    return TodoInDB(**todo)

@router.post("/todos", response_model=TodoInDB, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, current_user: str = Depends(get_current_user_id)):
    global next_todo_id
    new_todo = TodoInDB(id=next_todo_id, title=todo.title, completed=False, owner=current_user)
    todos_db[next_todo_id] = new_todo.dict()
    next_todo_id += 1
    return new_todo

@router.put("/todos/{todo_id}", response_model=TodoInDB)
async def update_todo(todo_id: int, todo_update: TodoUpdate, current_user: str = Depends(get_current_user_id)):
    existing_todo = get_todo_or_404_and_authorize(todo_id, current_user)

    update_data = todo_update.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    for key, value in update_data.items():
        existing_todo[key] = value

    return TodoInDB(**existing_todo)

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, current_user: str = Depends(get_current_user_id)):
    get_todo_or_404_and_authorize(todo_id, current_user)
    del todos_db[todo_id]
    return