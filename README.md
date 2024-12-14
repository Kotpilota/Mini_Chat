### Как запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/Kotpilota/Mini_Chat.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```

Обновить PIP

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
alembic revision --autogenerate -m "Initial revision"
alembic upgrade head
```

Запустить проект:

```
uvicorn app.main:app --reload
```
