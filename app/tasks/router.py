import os

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.tasks.dao import TaskDAO
from app.tasks.schemas import TasksCreate, TasksUpdate
from app.exceptions import TaskNotFoundException, TaskCreationException

script_dir = os.path.dirname(__file__)
templates_abs_path = os.path.join(script_dir, "../templates/")

router = APIRouter(prefix='/tasks', tags=['Задачи'])

templates = Jinja2Templates(directory=templates_abs_path)


@router.get("/", summary='Генерация страницы')
async def get_page(request: Request):
    return templates.TemplateResponse("task.html", context={'request': request})


@router.get("/list", summary="Получить все задачи")
async def get_tasks():
    tasks = await TaskDAO.find_all()
    return tasks


@router.get("/task/{task_id}", summary="Получить задачу по ID")
async def get_task_by_id(task_id: int):
    task = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task:
        raise TaskNotFoundException()
    return task


@router.post("/addTask", summary="Создать новую задачу")
async def create_task(task: TasksCreate):
    try:
        await TaskDAO.add(title=task.title, description=task.description)
        new_task = await TaskDAO.find_one_or_none(title=task.title, description=task.description)
        return new_task
    except Exception as e:
        raise TaskCreationException(detail=str(e))


@router.put("/editTask/{task_id}", summary="Обновить задачу по ID")
async def update_task(task_id: int, task: TasksUpdate):
    task_to_update = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task_to_update:
        raise TaskNotFoundException()
    await TaskDAO.update(task_to_update, task)
    updated_task = await TaskDAO.find_one_or_none_by_id(task_id)
    return updated_task


@router.delete("/deleteTask/{task_id}", summary="Удалить задачу по ID")
async def delete_task(task_id: int):
    task_to_delete = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task_to_delete:
        raise TaskNotFoundException()
    deleted_task = await TaskDAO.delete(task_id)
    return deleted_task
