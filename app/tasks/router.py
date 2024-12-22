from fastapi import APIRouter
from app.tasks.dao import TaskDAO
from app.tasks.schemas import TaskCreate, TaskUpdate
from app.exceptions import TaskNotFoundException, TaskCreationException

router = APIRouter(prefix='/tasks', tags=['Задачи'])

@router.post("/", summary="Создать новую задачу")
async def create_task(task: TaskCreate):
    try:
        new_task = await TaskDAO.add(title=task.title, description=task.description)
        return {'message': 'Задача успешно создана'}
    except Exception as e:
        raise TaskCreationException(detail=str(e))

@router.get("/", summary="Получить все задачи")
async def get_tasks():
    tasks = await TaskDAO.find_all()
    return tasks

@router.get("/{task_id}", summary="Получить задачу по ID")
async def get_task_by_id(task_id: int):
    task = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task:
        raise TaskNotFoundException()
    return task

@router.put("/{task_id}", summary="Обновить задачу по ID")
async def update_task(task_id: int, task: TaskUpdate):
    task_to_update = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task_to_update:
        raise TaskNotFoundException()
    updated_task = await TaskDAO.update(task_to_update, task)
    return {'message': 'Задача успешно отредактирована'}

@router.delete("/{task_id}", summary="Удалить задачу по ID")
async def delete_task(task_id: int):
    task_to_delete = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task_to_delete:
        raise TaskNotFoundException()
    deleted_task = await TaskDAO.delete(task_id)
    return {"msg": "Задача удалена", "task": deleted_task}
