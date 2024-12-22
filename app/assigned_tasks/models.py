from sqlalchemy import Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime


class AssignedTask(Base):
    __tablename__ = 'assigned_tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('tasks.id'))
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey('statuses.id'))
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
