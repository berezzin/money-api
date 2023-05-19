from httpx import AsyncClient
from sqlalchemy import insert, select

from src.transactions.models import Category, Transaction
from tests.conftest import async_session


async def test_add_category():
    async with async_session() as session:
        stmt = insert(Category).values(category_id=1, category_name='Food')
        await session.execute(stmt)
        await session.commit()

        query = select(Category)
        result = await session.scalars(query)
        new_category: Category = result.one_or_none()
        assert new_category.category_id == 1, 'Category has not been added'
        assert new_category.category_name == 'Food', 'Category has not been added'


async def test_add_transaction(ac: AsyncClient):
    auth_token = ac.cookies['money']

    response = await ac.post('/transaction/add',
                             json={
                                 "transaction_comment": "Spaghetti",
                                 "transaction_amount": 12.356,
                                 "transaction_category": 1
                             }, headers={'Cookie': f'money={auth_token}'})

    assert response.status_code == 200

    async with async_session() as session:
        query = select(Transaction)
        result = await session.scalars(query)
        new_transaction: Transaction = result.first()
        assert new_transaction.transaction_comment == "Spaghetti", 'Transaction has not been added'
        assert new_transaction.transaction_amount == 12.356, 'Transaction has not been added'
        assert new_transaction.transaction_category == 1, 'Transaction has not been added'
