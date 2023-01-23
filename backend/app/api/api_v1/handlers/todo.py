from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends

from backend.app.schemas.todo_schema import TodoOut, TodoCreate, TodoUpdate
from backend.app.models.user_model import User
from backend.app.deps.user_deps import get_current_user
from backend.app.services.todo_service import TodoService
from backend.app.models.todo_model import Todo


todo_router = APIRouter()


@todo_router.get('/', summary="get all todos of the user", response_model=List[TodoOut])
async def list_todos(current_user: User = Depends(get_current_user)):
    return await TodoService.list_todos(current_user)


@todo_router.post('/create', summary="create a todo", response_model=Todo)
async def create_todo(data: TodoCreate, current_user: User = Depends(get_current_user)):
    return await TodoService.create_todo(current_user, data)


@todo_router.get('/{todo_id}', summary="get a todo by todo_id", response_model=TodoOut)
async def retrieve(todo_id: UUID, current_user: User = Depends(get_current_user)):
    return await TodoService.retrieve_todo(current_user, todo_id)


@todo_router.put('/{todo_id}', summary="Update todo by todo_id", response_model=TodoOut)
async def update(todo_id: UUID, data: TodoUpdate, current_user: User = Depends(get_current_user)):
    return await TodoService.update_todo(current_user, todo_id, data)


@todo_router.delete('/{todo_id}', summary="Delete todo by todo_id")
async def delete(todo_id: UUID, current_user: User = Depends(get_current_user)):
    await TodoService.delete_todo(current_user, todo_id)
    return None
