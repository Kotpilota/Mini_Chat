from app.dao.base import BaseDAO
from app.UserTypes.models import UserType


class UserTypeDAO(BaseDAO):
    model = UserType