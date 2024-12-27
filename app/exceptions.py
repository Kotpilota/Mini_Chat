from fastapi import status, HTTPException


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")


class TokenNoFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден")


# Общие ошибки
class GenericException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


# Ошибки для задач
class TaskNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")


class TaskCreationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Ошибка при создании задачи: {detail}")


# Ошибки для статусов
class StatusNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Статус не найден")


class StatusCreationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Ошибка при создании статуса: {detail}")


# Ошибки для назначенных задач
class AssignedTaskNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Назначенная задача не найдена")


class AssignedTaskCreationException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail=f"Ошибка при создании назначенной задачи: {detail}")


UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')

PasswordMismatchException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пароли не совпадают!')

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валидный!')

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail='Не найден ID пользователя')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

NoUserTypeIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail='Не найден тип пользователя')


UserTypeAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Тип пользователя уже существует')

NoAssignedTaskException = HTTPException(status_code=404,
                                  detail="assigned_task doesn't exists!")

AssignedTaskAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                  detail="Задача уже существует!")

TaskAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                  detail="Задача уже существует!")

NoAssignedTaskExeption = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Задание уже задано")


TaskAlreadyExistsExeption = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                          detail="Задание уже существует")
