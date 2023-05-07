import datetime
import uuid
from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field
from sqlalchemy import select

from auth.auth import auth_backend
from auth.database import async_session
from auth.schemas import UserRead, UserCreate
from auth.user_manager import get_user_manager
from models import User, Transaction

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


transaction_router = APIRouter()


class TransactionSchema(BaseModel):
    user_id: str = Field(min_length=32, max_length=36)
    transaction_comment: str | None = Field(max_length=50, default=None)
    transaction_amount: float = 0
    transaction_category: int


@transaction_router.post('/add')
async def add_transaction(transaction_data: TransactionSchema):
    async with async_session() as session:
        new_transaction = Transaction(user_id=transaction_data.user_id,
                                      transaction_comment=transaction_data.transaction_comment,
                                      transaction_amount=transaction_data.transaction_amount,
                                      transaction_category=transaction_data.transaction_category)
        session.add(new_transaction)
        await session.commit()
        return {'Status': 200}


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
