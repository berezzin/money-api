from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, TIMESTAMP, Numeric, text
from sqlalchemy.orm import relationship

from src.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'users'

    username = Column(String(length=20), nullable=False)
    join_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    balance = Column(Numeric(precision=10, scale=3, asdecimal=False), nullable=False, server_default='0')

    transactions = relationship('Transaction', cascade='all, delete-orphan')
