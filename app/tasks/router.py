from fastapi import APIRouter, HTTPException

from app.tasks.dao import TaskDAO
from app.tasks.schemas import TaskCreate, TaskUpdate

router = APIRouter(prefix='/tasks', tags=['Tasks'])

@router.post("/", summary="Create a new task")
async def create_task(task: TaskCreate):
    try:
        new_task = await TaskDAO.add(title=task.title, description=task.description)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", summary="Get all tasks")
async def get_tasks():
    tasks = await TaskDAO.find_all()
    return tasks


@router.get("/{task_id}", summary="Get task by ID")
async def get_task_by_id(task_id: int):
    task = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", summary="Update task by ID")
async def update_task(task_id: int, task: TaskUpdate):
    task_to_update = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task_to_update:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = await TaskDAO.update(task_to_update, task)
    return updated_task


@router.delete("/{task_id}", summary="Delete task by ID")
async def delete_task(task_id: int):
    task_to_delete = await TaskDAO.find_one_or_none_by_id(task_id)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted_task = await TaskDAO.delete(task_id)
    return {"msg": "Task deleted", "task": deleted_task}
