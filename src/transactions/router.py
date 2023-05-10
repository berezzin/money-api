from fastapi import APIRouter

from src.database import async_session
from src.transactions.models import Transaction
from .schemas import TransactionSchema

router = APIRouter()


@router.post('/add')
async def add_transaction(transaction_data: TransactionSchema):
    async with async_session() as session:
        new_transaction = Transaction(user_id=transaction_data.user_id,
                                      transaction_comment=transaction_data.transaction_comment,
                                      transaction_amount=transaction_data.transaction_amount,
                                      transaction_category=transaction_data.transaction_category)
        session.add(new_transaction)
        await session.commit()
        return {'Status': 200}
