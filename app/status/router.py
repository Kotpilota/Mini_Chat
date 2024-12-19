from fastapi import APIRouter, HTTPException

from app.status.dao import StatusDAO
from app.status.schemas import StatusCreate, StatusUpdate

router = APIRouter(prefix='/status', tags=['Status'])

@router.post("/", summary="Create a new status")
async def create_status(status: StatusCreate):
    try:
        new_status = await StatusDAO.add(title=status.title)
        return new_status
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", summary="Get all statuses")
async def get_statuses():
    statuses = await StatusDAO.find_all()
    return statuses


@router.get("/{status_id}", summary="Get status by ID")
async def get_status_by_id(status_id: int):
    status = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status


@router.put("/{status_id}", summary="Update status by ID")
async def update_status(status_id: int, status: StatusUpdate):
    status_to_update = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status_to_update:
        raise HTTPException(status_code=404, detail="Status not found")
    updated_status = await StatusDAO.update(status_to_update, status)
    return updated_status


@router.delete("/{status_id}", summary="Delete status by ID")
async def delete_status(status_id: int):
    status_to_delete = await StatusDAO.find_one_or_none_by_id(status_id)
    if not status_to_delete:
        raise HTTPException(status_code=404, detail="Status not found")
    deleted_status = await StatusDAO.delete(status_id)
    return {"msg": "Status deleted", "status": deleted_status}
