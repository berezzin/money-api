from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from src.auth.models import User
from src.auth.router import current_user
from src.transactions.router import get_transactions_by_category_id

router = APIRouter()

templates = Jinja2Templates(directory='src/templates')


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/search/{category_id}')
def get_search_page(request: Request, transactions=Depends(get_transactions_by_category_id)):
    return templates.TemplateResponse('search.html', {'request': request, 'transactions': transactions.get('data')})


@router.get('/support/chat')
def get_support_chat_page(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse('support_chat.html', {'request': request, 'username': user.username})
