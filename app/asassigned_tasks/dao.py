from app.dao.base import BaseDAO
from app.asassigned_tasks.models import Assigned_task

class AssignedTaskDAO(BaseDAO):
    model = Assigned_task
