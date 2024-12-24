import os

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.exceptions import TokenExpiredException, TokenNoFoundException
from app.users.router import router as users_router
from app.chat.router import router as chat_router
from app.UserTypes.router import router as UsersTypeRouter
from app.assigned_tasks.router import router as asassigned_tasks_router
from app.status.router import router as status_router
from app.tasks.router import router as tasks_router

script_dir = os.path.dirname(__file__)
static_abs_path = os.path.join(script_dir, "static/")

app = FastAPI()
app.mount('/static', StaticFiles(directory=static_abs_path), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],
    # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(users_router)
app.include_router(chat_router)

app.include_router(UsersTypeRouter)

app.include_router(tasks_router)

app.include_router(status_router)

app.include_router(asassigned_tasks_router)

@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request,
                                          exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


# Обработчик для TokenNoFound
@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request,
                                           exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")
