import os

from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, \
    PasswordMismatchException, NoUserTypeIdException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth, SUserRead, UserUpdateType
from fastapi.templating import Jinja2Templates

script_dir = os.path.dirname(__file__)
templates_abs_path = os.path.join(script_dir, "../templates/")

router = APIRouter(prefix='/auth', tags=['Auth'])
templates = Jinja2Templates(directory=templates_abs_path)


@router.get('/', response_class=HTMLResponse, summary='Страница авторизации')
async def get_categories(request: Request):
    return templates.TemplateResponse('auth.html', {'request': request})


@router.get('/users')
async def get_users():
    users_all = await UsersDAO.find_all()
    return [{'id': user.id, 'name': user.name} for user in users_all]


@router.post('/register/')
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    if user_data.password != user_data.password_check:
        raise PasswordMismatchException('Пароли не совпадают')
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(name=user_data.name,
                       email=user_data.email,
                       hashed_password=hashed_password)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post('/login/')
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(check.id)})
    response.set_cookie(key='users_access_token', value=access_token, httponly=True)
    return {'ok': True,
            'access_token': access_token,
            'refresh_token': None,
            'message': 'Авторизация успешна!'}


@router.post('/logout/')
async def logout_user(response: Response):
    response.delete_cookie(key='users_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get('/users/page', response_class=HTMLResponse, summary='Страница пользователей')
async def get_users_page(request: Request):
    return templates.TemplateResponse('user.html', {'request': request})


@router.get('/users/list', response_model=list[SUserRead], summary='Получить список пользователей')
async def get_users_list():
    users_all = await UsersDAO.find_all()
    return [{'id': user.id, 'name': user.name, 'email': user.email, 'usertype': user.usertype} for user in users_all]


@router.put('/users/update/{user_id}', summary='Обновить тип пользователя')
async def update_user_type(user_id: int, data: UserUpdateType):
    user = await UsersDAO.find_one_or_none(id=user_id)
    if not user:
        raise NoUserTypeIdException

    await UsersDAO.update(user, {"usertype": data.usertype})
