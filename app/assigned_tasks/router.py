from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.users.dependencies import get_current_user
from app.assigned_tasks.dao import AssignedTaskDAO
from app.assigned_tasks.schemas import AssignedTaskCreate, AssignedTaskUpdate
from app.status.dao import StatusDAO
from app.exceptions import AssignedTaskNotFoundException, AssignedTaskCreationException

router = APIRouter(prefix='/assigned_tasks', tags=['Назначенные задачи'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/', summary='Страница ToDoList')
async def get_to_do_page(request: Request, User=Depends(get_current_user)):
    status_all = await StatusDAO.find_all()
    assigned_tasks_all = await AssignedTaskDAO.find_all()
    return templates.TemplateResponse('tasks.html', {
        'request': request,
        'status_all': status_all,
        'user': User,
        'assigned_tasks': assigned_tasks_all
    })


@router.post("/create", summary="Назначить задачу пользователю")
async def assign_task(assigned_task: AssignedTaskCreate):
    try:
        new_assigned_task = await AssignedTaskDAO.add(
            user_id=assigned_task.user_id,
            task_id=assigned_task.task_id,
            status_id=assigned_task.status_id,
            deadline=assigned_task.deadline
        )
        return {'message': 'Задача успешно назначена'}
    except Exception as e:
        raise AssignedTaskCreationException(detail=str(e))


@router.get("/list", summary="Получить все назначенные задачи")
async def get_assigned_tasks():
    assigned_tasks = await AssignedTaskDAO.find_all()
    return assigned_tasks


@router.get("/{assigned_task_id}", summary="Получить назначенную задачу по ID")
async def get_assigned_task_by_id(assigned_task_id: int):
    assigned_task = await AssignedTaskDAO.find_one_or_none_by_id(assigned_task_id)
    if not assigned_task:
        raise AssignedTaskNotFoundException()
    return assigned_task


@router.put("/update/{assigned_task_id}", summary="Обновить назначенную задачу по ID")
async def update_assigned_task(assigned_task_id: int, assigned_task: AssignedTaskUpdate):
    assigned_task_to_update = await AssignedTaskDAO.find_one_or_none_by_id(assigned_task_id)
    if not assigned_task_to_update:
        raise AssignedTaskNotFoundException()
    await AssignedTaskDAO.update(assigned_task_to_update, assigned_task)
    return {'message': 'Назначенная задача успешно изменена'}


@router.delete("/delete/{assigned_task_id}", summary="Удалить назначенную задачу по ID")
async def delete_assigned_task(assigned_task_id: int):
    assigned_task_to_delete = await AssignedTaskDAO.find_one_or_none_by_id(assigned_task_id)
    if not assigned_task_to_delete:
        raise AssignedTaskNotFoundException()
    deleted_assigned_task = await AssignedTaskDAO.delete(assigned_task_id)
    return {"msg": "Назначенная задача удалена", "assigned_task": deleted_assigned_task}
