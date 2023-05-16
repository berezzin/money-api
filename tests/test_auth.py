from sqlalchemy import insert, select

from src.transactions.models import Category
from tests.conftest import async_session


async def test_add_category():
    async with async_session() as session:
        stmt = insert(Category).values(category_id=1, category_name='Food')
        await session.execute(stmt)
        await session.commit()

        query = select(Category)
        result = await session.scalars(query)
        new_category: Category = result.one_or_none()
        assert new_category.category_id == 1
        assert new_category.category_name == 'Food'
