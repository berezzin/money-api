from sqlalchemy import Column, UUID, String, Boolean, TIMESTAMP, Numeric, text, ForeignKey, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import uuid

Base = declarative_base()
engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/money_db', echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(length=20), nullable=False)
    is_admin = Column(Boolean, default=False)
    join_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    balance = Column(Numeric(precision=10, scale=3, asdecimal=False), nullable=False, server_default='0')


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    transaction_comment = Column(String(length=50), nullable=True)
    transaction_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    transaction_amount = Column(Numeric(precision=10, scale=3, asdecimal=False), nullable=False, server_default='0')
    transaction_category = Column(Integer, ForeignKey('categories.category_id'))


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(length=15), nullable=False)
