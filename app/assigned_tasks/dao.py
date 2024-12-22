from datetime import datetime

from app.dao.base import BaseDAO
from app.assigned_tasks.models import AssignedTask
from app.tasks.dao import TaskDAO
from app.status.dao import StatusDAO


class AssignedTaskDAO(BaseDAO):
    model = AssignedTask

    @classmethod
    async def add_with_task(cls, user_id: int, status_id: int, deadline: datetime, title: str,
                            description: str):
        """
        Создает задачу, затем создаёт запись в assigned_tasks с привязкой к созданной задаче.
        """
        new_task = await TaskDAO.add(title=title, description=description)

        assigned_task = await cls.add(
            user_id=user_id,
            task_id=new_task.id,
            status_id=status_id,
            deadline=deadline
        )
        return assigned_task
