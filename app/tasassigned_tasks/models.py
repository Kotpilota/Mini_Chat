from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)


class Status(Base):
    __tablename__ = 'statuses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

class Assigned_task(Base):
    __tablename__ = 'assigned_tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('tasks.id'))
    status: Mapped[int] = mapped_column(Integer, ForeignKey('statuses.id'))
    deadline: Mapped[int] = mapped_column(TIMESTAMP, nullable=False)