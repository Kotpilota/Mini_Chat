from app.dao.base import BaseDAO
from app.tasks.models import Task


class TaskDAO(BaseDAO):
    model = Task
