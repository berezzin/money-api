import time
from email.message import EmailMessage

from celery import Celery
import smtplib

from src.config import REDIS_HOST, REDIS_PORT
from src.config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email_template_transactions(username: str, user_email: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = 'Transaction report'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        f'Good day, dear <b>{username}</b>!<br>'
        f'That is yours list of all transactions:',
        subtype='html'
    )

    return email


@celery.task()
def send_email_report_transactions(username: str, user_email: str):
    time.sleep(10)
    email = get_email_template_transactions(username, user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
