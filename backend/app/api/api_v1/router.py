from fastapi import APIRouter
from backend.app.api.api_v1.handlers import user
from backend.app.api.auth.jwt import auth_router
from backend.app.api.api_v1.handlers.todo import todo_router

router = APIRouter()

router.include_router(user.user_router, prefix='/users', tags=['users'])
router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(todo_router, prefix='/todo', tags=['todo'])
