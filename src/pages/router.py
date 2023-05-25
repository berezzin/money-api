from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from src.transactions.router import get_transactions_by_category_id

router = APIRouter()

templates = Jinja2Templates(directory='src/templates')


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/search/{category_id}')
def get_search_page(request: Request, transactions=Depends(get_transactions_by_category_id)):
    return templates.TemplateResponse('search.html', {'request': request, 'transactions': transactions.get('data')})
