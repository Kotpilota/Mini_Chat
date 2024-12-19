from app.dao.base import BaseDAO
from app.tasassigned_tasks.models import Task, Status, Assigned_task


class TaskDAO(BaseDAO):
    model = Task

class AssignedTaskDAO(BaseDAO):
    model = Assigned_task

class StatusDAO(BaseDAO):
    model = Status