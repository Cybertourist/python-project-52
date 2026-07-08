# Менеджер задач

[![Actions Status](https://github.com/Cybertourist/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Cybertourist/python-project-52/actions)
[![Sonar check](https://github.com/Cybertourist/python-project-52/actions/workflows/sonar-check.yml/badge.svg)](https://github.com/Cybertourist/python-project-52/actions/workflows/sonar-check.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Cybertourist_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Cybertourist_python-project-52)

Веб-приложение для управления задачами, построенное на Django.
Позволяет регистрировать пользователей, создавать задачи, назначать
им исполнителей, статусы и метки, а также фильтровать список задач
по статусу, исполнителю и меткам.

**Демо:** [приложение на Render](https://python-project-52.onrender.com)

## Возможности

- Регистрация, аутентификация и управление пользователями
- CRUD для задач, статусов и меток
- Назначение исполнителя и меток задаче
- Фильтрация задач по статусу, исполнителю, меткам и признаку «только свои задачи»
- Защита от удаления используемых статусов и меток
- Удалить задачу может только её автор

## Технологии

- Python 3.12+, Django
- PostgreSQL (продакшен) / SQLite (локальная разработка)
- Bootstrap 5, django-filter
- Gunicorn, WhiteNoise
- Rollbar (мониторинг ошибок)

## Требования

- Python 3.12 или новее
- [uv](https://docs.astral.sh/uv/)

## Установка

Клонируйте репозиторий и установите зависимости:

```bash
git clone https://github.com/Cybertourist/python-project-52.git
cd python-project-52
make install
```

Создайте файл `.env` в корне проекта:

```
SECRET_KEY=<ваш секретный ключ>
DEBUG=True
```

Дополнительно можно указать:

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
ROLLBAR_TOKEN=<токен Rollbar>
```

Примените миграции:

```bash
make migrate
```

## Запуск

Локальный сервер разработки:

```bash
make dev
```

Приложение будет доступно по адресу http://127.0.0.1:8000

Продакшен-сервер:

```bash
make render-start
```

## Тесты и линтер

```bash
uv run manage.py test
uv run ruff check .
```
