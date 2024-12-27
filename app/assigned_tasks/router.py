from fastapi import APIRouter, Response, HTTPException, status, Depends, \
    Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.exceptions import NoAssignedTaskExeption, TaskAlreadyExistsExeption, \
    AssignedTaskNotFoundException
from app.assigned_tasks.dao import AssignedTaskDAO
from app.tasks.dao import TaskDAO
from app.status.dao import StatusDAO
from app.assigned_tasks.schemas import (AssignedTasksCreate,
                                        AssignedTasksUpdate, \
    AssignedTasksRead)
from fastapi.templating import Jinja2Templates
from app.users.dependencies import \
    get_current_user  # Assuming you have user authentication
from typing import List, Any
import os
from app.users.models import User
from datetime import datetime

router = APIRouter(prefix="/assigned-tasks", tags=["AssignedTasks"])
templates = Jinja2Templates(directory='app/templates')


@router.get("/", response_class=HTMLResponse, summary="Страница задач")
async def get_categories(request: Request):
    return templates.TemplateResponse("tasks.html",
                                      {"request": request})


@router.get("/userId")
async def get_user_id(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/data/{user_id}")
async def get_assigned_tasks(user_id: int):
    assigned_tasks = await AssignedTaskDAO.find_all(user_id=user_id)
    list_as_tasks = [{"id": assigned_task.id,
                      "task_id": assigned_task.task_id,
                      "task_title": (await TaskDAO.find_one_or_none_by_id(
                          assigned_task.task_id)).title,
                      "status_id": assigned_task.status_id,
                      "status_title": (await StatusDAO.find_one_or_none_by_id(
                          assigned_task.status_id)).title}
                     for assigned_task in assigned_tasks]
    return list_as_tasks


@router.get("/assignedTasks/{assignedtasks_id}")
async def get_assigned_task_by_id(assignedtasks_id: int):
    assigned_task = await AssignedTaskDAO.find_one_or_none_by_id(
        assignedtasks_id)
    if not assigned_task:
        raise NoAssignedTaskExeption
    return {"id": assigned_task.id,
            "task_id": assigned_task.task_id,
            "task_title": (await TaskDAO.find_one_or_none_by_id(
                assigned_task.task_id)).title,
            "status_id": assigned_task.status_id,
            "status_title": (await StatusDAO.find_one_or_none_by_id(
                assigned_task.status_id)).title
            }


@router.post("/addAssignedTask/")
async def add_assigned_task(assigned_task: AssignedTasksCreate,
                            current_user: User = Depends(get_current_user)):
    existing_task = await TaskDAO.find_one_or_none(
        title=assigned_task.task_title)
    if existing_task:
        raise TaskAlreadyExistsExeption
    await TaskDAO.add(
        title=assigned_task.task_title,
        description="A"
    )
    atask = await AssignedTaskDAO.add(
        user_id=current_user.id,
        task_id=(await TaskDAO.find_one_or_none(
            title=assigned_task.task_title)).id,
        status_id=assigned_task.status_id,
        deadline=datetime(2024, 12, 26)
    )
    return atask


@router.put("/updateAssignedTask/{id}")
async def update_assigned_task(id: int, assigned_task: AssignedTasksUpdate):
    db_assigned_task = await AssignedTaskDAO.find_one_or_none_by_id(id)
    if not db_assigned_task:
        raise NoAssignedTaskExeption
    atask = await AssignedTaskDAO.update(db_assigned_task, assigned_task)
    return atask


@router.delete("/delete/{assigned_task_id}", summary="Удалить назначенную задачу по ID")
async def delete_assigned_task(assigned_task_id: int):
    assigned_task_to_delete = await AssignedTaskDAO.find_one_or_none_by_id(assigned_task_id)
    if not assigned_task_to_delete:
        raise AssignedTaskNotFoundException()
    deleted_assigned_task = await AssignedTaskDAO.delete(assigned_task_id)
    return {"msg": "Назначенная задача удалена", "assigned_task": deleted_assigned_task}
