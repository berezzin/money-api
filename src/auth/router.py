import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.auth.auth import auth_backend
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.auth.user_manager import get_user_manager

router = APIRouter()

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt"
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=""
)
