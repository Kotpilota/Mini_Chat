from fastapi import APIRouter
from app.status.dao import StatusDAO
from app.status.schemas import StatusCreate, StatusUpdate
from app.exceptions import StatusNotFoundException, StatusCreationException

router = APIRouter(prefix='/statuses', tags=['Статусы'])

@router.post("/", summary="Создать новый статус")
async def create_status(status: StatusCreate):
    try:
        new_status = await StatusDAO.add(title=status.title)
        return {'message': 'Статус успешно создан'}
    except Exception as e:
        raise StatusCreationException(detail=str(e))

@router.get("/", summary="Получить все статусы")
async def get_statuses():
    statuses = await StatusDAO.find_all()
    return statuses

@router.get("/{status_id}", summary="Получить статус по ID")
async def get_status_by_id(status_id: int):
    status = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status:
        raise StatusNotFoundException()
    return status

@router.put("/{status_id}", summary="Обновить статус по ID")
async def update_status(status_id: int, status: StatusUpdate):
    status_to_update = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status_to_update:
        raise StatusNotFoundException()
    updated_status = await StatusDAO.update(status_to_update, status)
    return {'message': 'Статус успешно отредактирован'}

@router.delete("/{status_id}", summary="Удалить статус по ID")
async def delete_status(status_id: int):
    status_to_delete = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status_to_delete:
        raise StatusNotFoundException()
    deleted_status = await StatusDAO.delete(status_id)
    return {"msg": "Статус удалён", "status": deleted_status}
