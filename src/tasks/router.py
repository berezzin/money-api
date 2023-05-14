from fastapi import APIRouter, Depends

from src.auth.models import User
from src.auth.router import current_user
from .tasks import send_email_report_transactions

router = APIRouter()


@router.get('/transactions')
async def send_transaction_report(user: User = Depends(current_user)):
    send_email_report_transactions.delay(user.id)
    return {'Status': 200,
            'data': 'Email has been sent',
            'details': None}
