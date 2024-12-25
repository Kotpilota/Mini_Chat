import os

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.status.dao import StatusDAO
from app.status.schemas import StatusCreate, StatusUpdate
from app.exceptions import StatusNotFoundException, StatusCreationException

script_dir = os.path.dirname(__file__)
templates_abs_path = os.path.join(script_dir, "../templates/")
router = APIRouter(prefix='/statuses', tags=['Статусы'])

templates = Jinja2Templates(directory=templates_abs_path)


@router.get('/', summary='Страница Status')
async def get_status_page(request: Request):
    return templates.TemplateResponse('status.html', {'request': request})


@router.get("/list", summary="Получить все статусы")
async def get_statuses():
    statuses = await StatusDAO.find_all()
    return statuses


@router.get("/status/{status_id}", summary="Получить статус по ID")
async def get_status_by_id(status_id: int):
    status = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status:
        raise StatusNotFoundException()
    return status


@router.post("/addStatus", summary="Создать новый статус")
async def create_status(status: StatusCreate):
    try:
        await StatusDAO.add(title=status.title)
        new_status = await StatusDAO.find_one_or_none(title=status.title)
        return new_status
    except Exception as e:
        raise StatusCreationException(detail=str(e))


@router.put("/editStatus/{status_id}", summary="Обновить статус по ID")
async def update_status(status_id: int, status: StatusUpdate):
    status_to_update = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status_to_update:
        raise StatusNotFoundException()
    await StatusDAO.update(status_to_update, status)

    updated_status = await StatusDAO.find_one_or_none(title=status.title)
    return updated_status


@router.delete("/deleteStatus/{status_id}", summary="Удалить статус по ID")
async def delete_status(status_id: int):
    status_to_delete = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status_to_delete:
        raise StatusNotFoundException()
    deleted_status = await StatusDAO.delete(status_id)
    return deleted_status
