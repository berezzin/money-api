from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory='src/templates')


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})
