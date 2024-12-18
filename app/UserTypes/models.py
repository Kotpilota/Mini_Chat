from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class UserType(Base):
    __tablename__ = 'users_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usertype: Mapped[String] = mapped_column(String, nullable=False)
