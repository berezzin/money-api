import asyncio
from email.message import EmailMessage
from uuid import UUID

from celery import Celery
import smtplib

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.auth.models import User
from src.config import REDIS_HOST, REDIS_PORT
from src.config import SMTP_USER, SMTP_PASSWORD
from src.database import async_session

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


async def get_email_template_transactions(user_id: UUID) -> EmailMessage:
    async with async_session() as session:
        stmt = select(User).where(User.id == user_id).options(selectinload(User.transactions))
        result = await session.scalars(stmt)
        user = result.first()
        user_transactions = user.transactions

        email = EmailMessage()
        email['Subject'] = 'Transaction report'
        email['From'] = SMTP_USER
        email['To'] = user.email

        email.set_content(
            f'Good day, dear <b>{user.username}</b>!<br>'
            f'That is yours list of all transactions:<br>'
            f'{[(transaction.transaction_comment, transaction.transaction_amount) for transaction in user_transactions]}',
            subtype='html'
        )

        return email


@celery.task()
def send_email_report_transactions(user_id: UUID):
    loop = asyncio.get_event_loop()
    email = loop.run_until_complete(get_email_template_transactions(user_id))
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
