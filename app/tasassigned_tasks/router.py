from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/assigned_tasks',tags=['Assigned Tasks'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse, summary='DO-to list')
async def get_categories(request: Request):
    return templates.TemplateResponse('tasks.html', {'request': request})
