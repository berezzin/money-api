import datetime
import uuid
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import select

from models import async_session, User, Transaction

app = FastAPI(title='Money API')

user_router = APIRouter()


class UserSchema(BaseModel):
    user_id: uuid.UUID
    username: str
    join_date: datetime.datetime
    balance: float

    class Config:
        orm_mode = True


@user_router.post('/')
async def create_user(username: str):
    async with async_session() as session:
        session.begin()
        new_user = User(username=username)
        session.add(new_user)
        await session.commit()
        return {'Id': new_user.user_id}


@user_router.get('/', response_model=Optional[UserSchema])
async def get_user(user_id: str) -> UserSchema | None:
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
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

main_router.include_router(user_router, prefix='/user', tags=['Users'])
main_router.include_router(transaction_router, prefix='/transaction', tags=['Transactions'])
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
