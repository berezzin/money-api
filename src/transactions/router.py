import time

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.transactions.models import Transaction
from .schemas import TransactionSchema
from ..auth.models import User
from ..auth.router import current_user

router = APIRouter()


@router.post('/add')
async def add_transaction(transaction_data: TransactionSchema,
                          user: User = Depends(current_user),
                          session: AsyncSession = Depends(get_async_session)):
    new_transaction = Transaction(user_id=user.id,
                                  transaction_comment=transaction_data.transaction_comment,
                                  transaction_amount=transaction_data.transaction_amount,
                                  transaction_category=transaction_data.transaction_category)
    session.add(new_transaction)
    await session.commit()
    return {'Status': 200}


@router.get('/')
@cache(expire=5)
def long_cached_operation():
    time.sleep(2)
    return {'Status': 'OK'}
