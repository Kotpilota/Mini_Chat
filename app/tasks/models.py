from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True,
                                    autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
