from typing import List

from fastapi import APIRouter, Response, status

from app.UserTypes.dao import UserTypeDAO
from app.UserTypes.schemas import UserTypeRead, UserTypeCreate, UserTypeUpdate
from app.exceptions import NoUserTypeIdException, \
    UserTypeAlreadyExistsException

router = APIRouter(prefix='/utype', tags=['Utype'])


@router.get('/usertypes/{usertype_id}', response_model=UserTypeRead)
async def get_usertype(usertype_id: int):
    usertype = await UserTypeDAO.find_one_or_none(id=usertype_id)

    if not usertype:
        raise NoUserTypeIdException

    return UserTypeRead(id=usertype.id, usertype=usertype.usertype)


@router.get('/usertypes', response_model=List[UserTypeRead])
async def get_usertypes():
    user_types_all = await UserTypeDAO.find_all()
    return user_types_all


@router.post('/addUserType/')
async def create_usertype(user_type: UserTypeCreate):
    existing_usertype = await UserTypeDAO.find_one_or_none(
        usertype=user_type.usertype)
    if existing_usertype:
        raise UserTypeAlreadyExistsException

    await UserTypeDAO.add(usertype=user_type.usertype)

    return {'message': 'ok'}


@router.put("/updateUserType/{id}")
async def update_user_type(id: int, user_type: UserTypeUpdate):
    db_user_type = await UserTypeDAO.find_one_or_none_by_id(data_id=id)
    if not db_user_type:
        raise NoUserTypeIdException

    await UserTypeDAO.update(db_user_type, user_type)

    return {'message': 'ok'}


@router.delete("/deleteUserType/{usertype_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_type(usertype_id: int):
    user_type = await UserTypeDAO.delete(usertype_id)
    if not user_type:
        raise NoUserTypeIdException
    return Response(status_code=status.HTTP_204_NO_CONTENT)
