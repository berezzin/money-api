import datetime
import uuid
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field
from sqlalchemy import select

from src.auth.auth import auth_backend
from .database import async_session
from src.auth.schemas import UserRead, UserCreate
from src.auth.user_manager import get_user_manager
from .auth.models import User

from .transactions.router import router as transaction_router

app = FastAPI(title='Money API')

user_router = APIRouter()


class UserSchema(BaseModel):
    id: uuid.UUID
    username: str
    join_date: datetime.datetime
    balance: float

    class Config:
        orm_mode = True


@user_router.post('/')
async def create_user(username: str, email: str, hashed_password: str):
    async with async_session() as session:
        session.begin()
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        session.add(new_user)
        await session.commit()
        return {'Id': new_user.id}


@user_router.get('/', response_model=Optional[UserSchema])
async def get_user(user_id: str) -> UserSchema | None:
    async with async_session() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.scalars(stmt)
        user = result.first()
        return user


main_router = APIRouter()

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@main_router.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


main_router.include_router(user_router, prefix='/user', tags=['Users'])
main_router.include_router(transaction_router, prefix='/transaction', tags=['Transactions'])
main_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
main_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
