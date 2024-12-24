from typing import List
import os

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from idna.idnadata import scripts

from app.UserTypes.dao import UserTypeDAO
from app.UserTypes.schemas import UserTypeRead, UserTypeCreate, UserTypeUpdate
from app.exceptions import NoUserTypeIdException, \
    UserTypeAlreadyExistsException

script_dir = os.path.dirname(__file__)
templates_abs_path = os.path.join(script_dir, "../templates/")

router = APIRouter(prefix='/usertype', tags=['UserType'])
templates = Jinja2Templates(directory=templates_abs_path)


@router.get('/', summary='Страница UserType')
async def get_user_types(request: Request):
    return templates.TemplateResponse('usertype.html', {'request': request})


@router.get('/type/{usertype_id}', response_model=UserTypeRead,
            summary='Получить тип пользователя по ID')
async def get_usertype(usertype_id: int):
    usertype = await UserTypeDAO.find_one_or_none(id=usertype_id)

    if not usertype:
        raise NoUserTypeIdException

    return UserTypeRead(id=usertype.id, usertype=usertype.usertype)


@router.get('/list', response_model=List[UserTypeRead], summary='Получить все типы пользователя')
async def get_usertypes():
    usertypes = await UserTypeDAO.find_all()
    return usertypes


@router.post('/addUserType', summary='Создать тип пользователя')
async def create_usertype(user_type: UserTypeCreate):
    existing_usertype = await UserTypeDAO.find_one_or_none(
        usertype=user_type.usertype)
    if existing_usertype:
        raise UserTypeAlreadyExistsException

    await UserTypeDAO.add(usertype=user_type.usertype)

    new_user_type = await UserTypeDAO.find_one_or_none(usertype=user_type.usertype)

    return new_user_type


@router.put("/updateUserType/{id}", summary='Отредактировать тип пользователя')
async def update_user_type(id: int, user_type: UserTypeUpdate):
    db_user_type = await UserTypeDAO.find_one_or_none_by_id(data_id=id)
    if not db_user_type:
        raise NoUserTypeIdException

    await UserTypeDAO.update(db_user_type, user_type)

    updated_user_type = await UserTypeDAO.find_one_or_none(usertype=user_type.usertype)
    return updated_user_type


@router.delete("/deleteUserType/{usertype_id}", summary='Удалить тип пользователя')
async def delete_user_type(usertype_id: int):
    user_type = await UserTypeDAO.delete(usertype_id)
    if not user_type:
        raise NoUserTypeIdException()
    return user_type
