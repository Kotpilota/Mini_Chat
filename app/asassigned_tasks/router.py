from fastapi import APIRouter, HTTPException

from app.asassigned_tasks.dao import AssignedTaskDAO
from app.asassigned_tasks.schemas import AssignedTaskCreate, AssignedTaskUpdate

router = APIRouter(prefix='/assigned_tasks', tags=['AssistedTasks'])


@router.post("/", summary="Создание задачи")
async def assign_task(assigned_task: AssignedTaskCreate):
    try:
        new_assigned_task = await AssignedTaskDAO.add(
            user_id=assigned_task.user_id,
            task_id=assigned_task.task_id,
            status=assigned_task.status,
            deadline=assigned_task.deadline
        )
        return new_assigned_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", summary="Все задачи")
async def get_assigned_tasks():
    assigned_tasks = await AssignedTaskDAO.find_all()
    return assigned_tasks


@router.get("/{assigned_task_id}", summary="Задача")
async def get_assigned_task_by_id(assigned_task_id: int):
    assigned_task = await AssignedTaskDAO.find_one_or_none_by_id(assigned_task_id)
    if not assigned_task:
        raise HTTPException(status_code=404, detail="Assigned Task not found")
    return assigned_task


@router.put("/{assigned_task_id}", summary="Изменение задачи")
async def update_assigned_task(assigned_task_id: int, assigned_task: AssignedTaskUpdate):
    assigned_task_to_update = await AssignedTaskDAO.find_one_or_none_by_id(assigned_task_id)
    if not assigned_task_to_update:
        raise HTTPException(status_code=404, detail="Assigned Task not found")
    updated_assigned_task = await AssignedTaskDAO.update(assigned_task_to_update, assigned_task)
    return updated_assigned_task


@router.delete("/{assigned_task_id}", summary="Удаление задачи")
async def delete_assigned_task(assigned_task_id: int):
    assigned_task_to_delete = await AssignedTaskDAO.find_one_or_none_by_id(assigned_task_id)
    if not assigned_task_to_delete:
        raise HTTPException(status_code=404, detail="Assigned Task not found")
    deleted_assigned_task = await AssignedTaskDAO.delete(assigned_task_id)
    return {"msg": "Assigned Task deleted", "assigned_task": deleted_assigned_task}
