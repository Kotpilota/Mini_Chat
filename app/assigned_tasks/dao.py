from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.assigned_tasks.models import AssignedTask
from app.dao.base import BaseDAO
from app.database import get_db
from app.tasks.dao import TaskDAO


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

    @staticmethod
    async def find_all_with_task_titles():
        """
        Возвращает все назначенные задачи с предзагруженным названием задач (task.title).
        """
        async for db_session in get_db():
            result = await db_session.execute(
                select(AssignedTask).options(
                    selectinload(AssignedTask.task)  # Предзагрузка связанных задач
                )
            )
            assigned_tasks = result.scalars().all()

            # Добавляем поле task_title в каждый объект
            return [
                {
                    "id": task.id,
                    "user_id": task.user_id,
                    "status_id": task.status_id,
                    "deadline": task.deadline,
                    "task_title": task.task.title if task.task else None,
                }
                for task in assigned_tasks
            ]