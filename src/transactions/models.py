from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, Numeric, text

from src.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(GUID, ForeignKey('users.id'))
    transaction_comment = Column(String(length=50), nullable=True)
    transaction_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    transaction_amount = Column(Numeric(precision=10, scale=3, asdecimal=False), nullable=False, server_default='0')
    transaction_category = Column(Integer, ForeignKey('categories.category_id'))


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(length=15), nullable=False)
